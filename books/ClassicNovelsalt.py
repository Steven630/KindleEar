#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return Classicalt
    

class Classicalt(BaseFeedBook):
    title                 =  u'古代小说网sohu'
    description           =  u'刊发中国古代小说、戏曲、说唱、文史哲方面的文章'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
    oldest_article        = 1
#    deliver_days          = ['Friday']
#    deliver_times         = [18]
    fulltext_by_readability = False
    keep_image            =  True
    keep_only_tags = [
                      dict(name='div', attrs={'class': 'text'})
                     ]
    remove_tags = [ dict(id='backsohucom')]
    remove_tags_after =[dict(id='backsohucom')]
    remove_classes = ['article-info']
    
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'http://mp.sohu.com/profile?xpt=bWhtaW5nMUBzb2h1LmNvbQ==&_f=index_pagemp_1'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
        for article in soup.find_all('div', class_='content_wrap', limit=6):
            timestamp = article.find('div', class_='wrap_mark')
            span= timestamp.find('span')
            timestamp = string_of_tag(span).strip()
            if u'今天' not in timestamp and u'昨天' not in timestamp:
                continue
            div = article.find('div', class_='wrap_title')
            a = span.find('a', href=True)
            title = string_of_tag(a).strip()
            if not title:
                self.log.warn('This title not found.')
                continue
            url = a['href']
            if url.startswith('/'):
                url = 'http:' + url
            urls.append((u'古代小说网sohu',title,url,None))
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
