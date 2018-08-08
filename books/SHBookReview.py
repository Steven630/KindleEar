#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return Bookreview
    

class Bookreview(BaseFeedBook):
    title                 =  u'上海书评'
    description           =  u'上海书评'
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
                      dict(attrs={'class':'news_txt'})
                     ]
    extra_css= '''
    .x-editable {font-style: italic;}
    span {text-indent: 0em; font-style: italic;}
    p { text-indent: 2em; margin-bottom: 2em; }
    img { text-indent: 0em; text-align: center;}
    .contheight { height: 16px; width: 100%;}
    .news_txt { text-indent: 2em; font-size: 1rem; line-height: 150%;}
    div { display: block;}
    h1 { text-align: center;}
        '''
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'http://www.thepaper.cn/list_masonry.jsp?nodeid=26878'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
            
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
        for article in soup.find_all('div', class_='news_li', limit=6):
            inter = article.find('div', class_='pdtt_trbs')
            timestamp = inter.find('span')
            timestamp = string_of_tag(timestamp).strip()
            if u'天' in timestamp or u'-' in timestamp:
                continue
            h2 = article.find('h2')
            a = h2.find('a', href=True)
            title = string_of_tag(a).strip()
            if not title:
                self.log.warn('This title not found.')
                continue
            url = a['href']
            if url.startswith(r'news'):
                url = 'http://www.thepaper.cn/' + url
            urls.append((u'上海书评',title,url,None))
        if len(urls) == 0:
            self.log.warn('No article found for Shanghai Book Review.')
        return urls
