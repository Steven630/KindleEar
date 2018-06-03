#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return PhoenixW
    

class PhoenixW(BaseFeedBook):
    title                 =  u'凤凰周刊'
    description           =  u'凤凰周刊微信'
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
                      dict(name='h1'),
                      dict(id='js_content')
                     ]
#     remove_tags_after =[dict(name='section', attrs={'style': re.compile('box-sizing: border-box; background-color: rgb(255, 255, 255);')})]
#     remove_tags = [dict(name='section', attrs={'style': re.compile('box-sizing: border-box; background-color: rgb(255, 255, 255);')})]
    remove_tags_after =[dict(name='span', string=u'- END -')]
    remove_tags = [dict(name='span', string=u'- END -')]
    
    
#    remove_tags = [{'name':'section'}]
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'http://www.jintiankansha.me/column/sL2XnLMwub'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
        section = soup.find('div', class_='entries')
        for article in section.find_all('div', class_='cell item', limit=10):
            timestamp = article.find('span', class_='small fade')
            timestamp = string_of_tag(timestamp).strip()
#            if u'小时' not in timestamp and u'昨天' not in timestamp:
            if u'小时' not in timestamp:
                continue
            span = article.find('span', class_='item_title')
            a = span.find('a', href=True)
            title = string_of_tag(a).strip()
            if not title:
                self.log.warn('This title not found.')
                continue
            if u'[原创]' not in title:
                continue
            if u'订阅有礼' in title or u'《凤凰周刊》' in title:
                continue
            url = a['href']
            urls.append((u'凤凰Weekly',title,url,None))
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
