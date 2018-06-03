#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return Comparee
    

class Comparee(BaseFeedBook):
    title                 =  u'社论比较'
    description           =  u'韩国报纸社论比较，每周二推送。'
    language              = 'ko'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
    oldest_article        = 1
    deliver_days          = ['Tuesday']
#    deliver_times         = [18]
    fulltext_by_readability = False
    keep_image            =  False
    
    keep_only_tags = [
#                      dict(name='h1'),
                      dict(id='article_body'),
#                      dict(attrs={'class':['article-wrap article-wrap2 article-font3','article-wrap']})
#                       dict(name='div', attrs={'itemprop':['articleBody']})
#                      dict(id='article-body-blocks')
                     ]
    remove_classes = ['ab_photo photo_left']
    
    extra_css      = '''
        body { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        p { font-size: 1em;  text-align: justify;  line-height: 1.718em }
        div { font-size: 1em;  text-align: justify;  line-height: 1.718em }
        .ab_sub_heading { font-size: large; font-weight: bold  }
        .caption {font-style: italic}
        '''
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'http://news.joins.com/Issue/10061'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
        for article in soup.find_all('strong', class_='headline mg', limit=4): #只保留最近一个月的四篇
            a = article.find('a', href=True)
            title = string_of_tag(a).strip()
            if not title:
                self.log.warn('This title not found.')
                continue
            url = a['href']
            if url.startswith('/'):
                url = 'http://news.joins.com' + url
            urls.append((u'사설 속으로',title,url,None))
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
