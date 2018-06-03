#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return YonhapChina
    

class YonhapChina(BaseFeedBook):
    title                 =  u'韩联社中国新闻'
    description           =  u'韩联社中国新闻'
    language              = 'ko'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8-sig"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
    oldest_article        = 1
    fulltext_by_readability = False
    keep_image            =  True
    extra_css      = '''
        body { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        p { font-size: 1em;  text-align: justify;  line-height: 1.718em }
        div { font-size: 1em;  text-align: justify;  line-height: 1.718em }
        h1 { font-size: large  }
        '''
    keep_only_tags = [
#                      dict(name='h1'),
                      dict(id='articleWrap'),
                      dict(attrs={'class':['article-wrap article-wrap2 article-font3','article-wrap']})
#                       dict(name='div', attrs={'itemprop':['articleBody']})
#                      dict(id='article-body-blocks')
                     ]
    remove_classes = ['share-info','link-info','article-ad-box','adrs','article-sns-md','cprgt','pblsh','article-sns-md sns-md03',
                      'img-info','banner-0-wrap','blind'
                     ]
    remove_tags_after = [ dict(attrs={'class':[
            'pblsh'
    ]})]
    
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        main = 'http://www.yonhapnews.co.kr/international/0603000001.html'
        urls = []
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch mainnews failed:%s'%main)
            
        content = result.content.decode(self.page_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
        section = soup.find('div', attrs={'class':'headlines headline-list'})
        for article in section.find_all('li', attrs={'class':'section02'}):
            if article is None:
                self.log.warn('This article not found')
                continue
            ptime= article.find('span', attrs={'class':'p-time'})
            if ptime:
                ptime= string_of_tag(ptime).strip()
            strong = article.find('strong', attrs={'class':'news-tl'})
            a = strong.find('a', href=True)
            atitle = string_of_tag(a).strip()
            atitle = atitle + ' ' + ptime
            url = a['href']
            urls.append((u'중국 뉴스',atitle,url,None))        
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
