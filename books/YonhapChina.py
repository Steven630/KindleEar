#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import datetime

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
    keep_image            =  False
    extra_css      = '''
        p { font-size: 1em; font-weight: 600;  text-align: justify;  line-height: 1.5 }
        h1 { font-size: large  }
        '''
    keep_only_tags = [
                      dict(name='h1'),
                      dict(id='articleWrap'),
                      dict(attrs={'class':['story-news article']})
#                       dict(name='div', attrs={'itemprop':['articleBody']})
#                      dict(id='article-body-blocks')
                     ]
    remove_classes = ['share-info','link-info','article-ad-box','adrs','article-sns-md','cprgt','pblsh','article-sns-md sns-md03',
                      'img-info','banner-0-wrap','blind','article-sns-md sns-md04','adrs txt-copyright'
                     ]
    remove_tags_after = [ dict(attrs={'class':[
            'adrs txt-copyright'
    ]})]
    
    
    def ParseFeedUrls(self):
        #return lists like [(section,title,url,desc),..]
        mainhead = 'https://www.yna.co.kr/international/china/'
        num =1
        urls = []
        callitaday = False
        koreanow = datetime.datetime.utcnow()+ datetime.timedelta(hours=9)
        koreadate = koreanow.date()
        year = koreanow.year
        
        while not callitaday:
            main = mainhead + str(num)
            opener = URLOpener(self.host, timeout=90)
            result = opener.open(main)
            if result.status_code != 200:
                self.log.warn('fetch mainnews failed:%s'%main)

            content = result.content.decode(self.page_encoding)
            soup = BeautifulSoup(content, "lxml")
            #开始解析

            section = soup.find('div', class_='list-type038')
            for article in section.find_all('div', class_='item-box01'):
                if article is None:
                    self.log.warn('This article not found')
                    continue
                ptime= article.find('span', class_='txt-time')
                if ptime:
                    ptime= string_of_tag(ptime).strip()
                    pdate=ptime[0:5] #只要07-30这样的日期
                    pdate= str(year) + '-'+ pdate #加上年份，否则默认1900年
                    pdate = datetime.datetime.strptime(pdate, '%Y-%m-%d').date()
                    delta=(koreadate-pdate).days
                    if self.oldest_article > 0 and delta >= self.oldest_article:
                        callitaday = True
                        break #因为是按时间顺序的
                newscon = article.find('div', class_='news-con')
                a = newscon.find('a', href=True)
                atitle = string_of_tag(a).strip()
                atitle = atitle + ' ' + ptime[6:] #只保留点钟
                url = a['href']
                if url.startswith('/'):
                    url= 'https:'+ url
                urls.append((u'중국 뉴스',atitle,url,None))
            num = num + 1
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
