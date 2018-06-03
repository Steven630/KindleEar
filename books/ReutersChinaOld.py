#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import datetime

def getBook():
    return Reuters
    

class Reuters(BaseFeedBook):
    title                 = 'Reuters China Old'
    description           = 'Reuters China Old'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
    oldest_article        = 1
#    deliver_days          = ['Friday']
#    deliver_times         = [18]
    fulltext_by_readability = True
    keep_image            =  False
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'http://uk.reuters.com/places/china'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
#        for section in soup.find_all('div', attrs={'class':'topStory'}):
        section = soup.find('div', attrs={'class':'topStory'})
        toparticle = section.find('a', href=True)
        if toparticle is None:
            self.log.warn('Top news not found')
        toptitle = string_of_tag(toparticle).strip()
        if not toptitle:
            self.log.warn('No top story title')
        url = toparticle['href']
        if url.startswith(r'/'):
            url = 'http://uk.reuters.com' + url
        urls.append(('Reuters China',toptitle,url,None))
            
#        for sect in soup.find_all('div', id='moreSectionNews'):
        sect=soup.find('div', id='moreSectionNews')
        for feature in sect.find_all('div', attrs={'class':'feature'}):
            article = feature.find('a', href=True)
            title = string_of_tag(article).strip()
            url = article['href']
            timestamp = feature.find('span', attrs={'class':'timestamp'})
            if not timestamp:
                continue
            timestamp = string_of_tag(timestamp).strip()
            #今天的文章
            if 'pm' in timestamp or 'am' in timestamp:
                delta=0
            else:
                pubtime = datetime.datetime.strptime(timestamp, '%d %b %Y').date()
                tnow = datetime.datetime.utcnow()
                tnow = tnow.date()
                delta=(tnow-pubtime).days
            if self.oldest_article > 0 and delta > self.oldest_article:
                continue
            if url.startswith(r'/'):
                url = 'http://uk.reuters.com' + url
                #self.log.info('\tFound article:%s' % title)
            urls.append(('Reuters China',title,url,None))                
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
    
    extra_css= '''
    h1 {font-size: large; font-weight: bold}
    .article-subtitle { font-weight: bold }
    .module-caption {font-style: italic}
    h3 {font-size: medium; font-weight: bold}
    figcaption {font-style: italic}
    .Image_caption_KoNH1 {font-style: italic}
    '''
