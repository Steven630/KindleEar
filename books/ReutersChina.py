#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import re

def getBook():
    return ReutersChinaN
    

class ReutersChinaN(BaseFeedBook):
    title                 = 'Reuters China'
    description           = 'Reuters China'
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
                      dict(attrs={'class':'body_1gnLA'})
                     ]
    remove_classes = [ re.compile('^DPSlot'), re.compile('^Attribution'), 'StandardArticleBody_trustBadgeContainer_1gqgJ','Slideshow_count_3OPtf',
                       re.compile('^RelatedCoverage'), re.compile('^Slideshow'), re.compile('^Video_container'), re.compile('^PrimaryAsset_container'),
                       re.compile('^trustBadgeContainer'), re.compile('^inline-container'), re.compile('^related-coverage'), 
                       re.compile('^attribution_')
                     ]
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'https://www.reuters.com/places/china'
        urls = []
        urladded = set()
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析           
        for item in soup.find_all('div', attrs={'class':'image-story-container_2baSf'}):
            timestamp = item.find('span', attrs={'class':'date-updated_1EZPz'})
            if not timestamp:
                continue
            timestamp = string_of_tag(timestamp).strip()
            #今天的文章
            if 'hour' not in timestamp and 'minute' not in timestamp:
                continue
            h2 = item.find('h2')
            article = h2.find('a', href=True)
            title = string_of_tag(article).strip()
            url = article['href']
            if url.startswith(r'/'):
                url = 'https://www.reuters.com' + url
                #self.log.info('\tFound article:%s' % title)
            if url not in urladded:
                urls.append(('Reuters China',title,url,None))
                urladded.add(url)
        if len(urls) == 0:
            self.log.warn('Failed to find articles for Reuters China.')
        return urls
    
    extra_css= '''
    h1 {font-size: large; font-weight: bold}
    .article-subtitle { font-weight: bold }
    .module-caption {font-style: italic}
    h3 {font-size: medium; font-weight: bold}
    figcaption {font-style: italic}
    .caption_KoNH1 {font-style: italic}
    '''
