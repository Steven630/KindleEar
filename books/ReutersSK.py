#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import datetime
import re

def getBook():
    return Reuters
    

class Reuters(BaseFeedBook):
    title                 = 'Reuters South Korea'
    description           = 'Reuters South Korea'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
    oldest_article        = 1
#    deliver_days          = ['Friday']
#    deliver_times         = [18]
    fulltext_by_readability = False
    keep_image            =  False
    keep_only_tags = [
                      dict(name='h1'),
                      dict(attrs={'class':'StandardArticleBody_body'})
                     ]
    remove_classes = [ re.compile('^DPSlot'), re.compile('^Attribution'), 'StandardArticleBody_trustBadgeContainer_1gqgJ','Slideshow_count_3OPtf',
                       re.compile('^RelatedCoverage'), re.compile('^Slideshow'), re.compile('^Video_container'), re.compile('^PrimaryAsset_container'),
                       re.compile('^trustBadgeContainer'), re.compile('^inline-container'), re.compile('^related-coverage'), 
                       re.compile('^attribution_'),'StandardArticleBody_trustBadgeContainer'
                     ]
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'https://www.reuters.com/places/south-korea'
        urls = []
        isEST = False #判断是EST还是EDT
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        soup = soup.find('div', class_='column1 col col-10')
        if not soup:
            self.log.warn('Failed to find column1 col col-10 for ReutersSK.')
        
        #开始解析
        section=soup.find('div', class_='story-content')
        if section:
            toparticle = section.find('a', href=True)
            if toparticle is None:
                self.log.warn('Top news not found')
            toptitle = string_of_tag(toparticle).strip()
            if not toptitle:
                self.log.warn('No top story title')
            url = toparticle['href']
            if url.startswith(r'/'):
                url = 'http://www.reuters.com' + url
            urls.append(('Reuters South Korea',toptitle,url,None))
        else:
            self.log.warn('Top story not found for ReutersSK.')
            
        sect=section.find_next('section', class_='module-content')
        for feature in sect.find_all('div', attrs={'class':'story-content'}):
            article = feature.find('a', href=True)
            title = string_of_tag(article).strip()
            url = article['href']
            timestamp = feature.find('span', attrs={'class':'timestamp'})
            if not timestamp:
                continue
            timestamp = string_of_tag(timestamp).strip()
            #今天的文章
            if 'EDT' in timestamp or 'EST' in timestamp:
                delta=0
                if 'EST' in timestamp:
                    isEST=True
            else:
                pubtime = datetime.datetime.strptime(timestamp, '%b %d %Y').date()
                #默认为EDT
                tnow = datetime.datetime.utcnow()-datetime.timedelta(hours=4)
                currentmonth= tnow.month
                if currentmonth in [1, 2, 12] or isEST:
                    tnow = datetime.datetime.utcnow()-datetime.timedelta(hours=5)
                tnow = tnow.date()
                delta=(tnow-pubtime).days
            if self.oldest_article > 0 and delta > self.oldest_article:
                continue
            if url.startswith(r'/'):
                url = 'https://www.reuters.com' + url
                #self.log.info('\tFound article:%s' % title)
            urls.append(('Reuters South Korea',title,url,None))
                                
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
    
    extra_css= '''
    h1 {font-size: large; font-weight: bold}
    .article-subtitle { font-weight: bold }
    .module-caption {font-style: italic}
    h3 {font-size: medium; font-weight: bold}
    figcaption {font-style: italic}
    .Image_caption {font-style: italic}
    .caption_KoNH1 {font-style: italic}
    '''
