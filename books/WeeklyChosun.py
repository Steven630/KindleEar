#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import urllib

def getBook():
    return ChosunWeekly
    

def fetch_cover(self):
    mainurl = 'http://weekly.chosun.com'
    opener = URLOpener(None, timeout=180)
#   opener = URLOpener(self.host, timeout=90)
    result = opener.open(mainurl)
    content = result.content.decode('euc-kr')
    soup = BeautifulSoup(content, "lxml")
    div = soup.find('div', class_='box_cover_new')
    img = div.find('img', src=True)
    cover = img.get('src')
    if cover.startswith('/'):
        cover = mainurl + cover
    else:
        cover = 'http://weekly.chosun.com/'+ cover
    data = urllib.urlopen(cover).read()
    return data

    
class ChosunWeekly(BaseFeedBook):
    title                 =  u'周刊朝鲜'
    description           =  u'每周三投递'
    language              = 'ko'
    feed_encoding         = "euc-kr"
    page_encoding         = "euc-kr"
    mastheadfile          = "mh_economist.gif" 
#    coverfile             = "cv_economist.jpg"
    coverfile             =  fetch_cover
    deliver_days          = ['Wednesday']
    deliver_times         = [14]
    fulltext_by_readability = False
    keep_image            = True
    needs_subscription    = False
    
         
    
    keep_only_tags = [{'name':'h2'},
                      dict(name='div', attrs={'class': 'article_body' })]
#    feeds = [('Index', 'http://weekly.chosun.com/client/news/alllst.asp?nHo=') ]

    def ParseFeedUrls(self):
        #return list like [(section,title,url,desc),..]
        def FindHo():
            hopage = 'http://weekly.chosun.com/client/contents/lst.asp'
            opener = URLOpener(self.host, timeout=90)
            result = opener.open(hopage)
            content = result.content.decode('euc-kr')
            if result.status_code != 200:
                self.log.warn('fetching hopage failed:%s'%hopage)
            soup = BeautifulSoup(content, "lxml")
            location=soup.find('div', id='Location')
            edition=location.find('div', class_='edition')
            ho = string_of_tag(edition).strip()
            if ho.startswith('['):
                ho=ho[1:5]
            else:
                self.log.warn('Fetching ho failed.')
            return ho
        
        mainhead = 'http://weekly.chosun.com/client/news/alllst.asp?nHo='
        urls = []
        urladded = set()
        opener = URLOpener(self.host, timeout=90)
        ho = FindHo()
        main= mainhead + ho
        result= opener.open(main)
        if result.status_code != 200:
            self.log.warn('Fetching TOC failed:%s'%main)
            return []
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")

        #开始解析
        def tr_has_a_tag(tag):
            return tag.name=='tr' and tag.find('a')
        listarea= soup.find('div', class_='List_area')    
        for section in listarea.find_all('table'):
            h4 = section.find_previous_sibling('h4')
            sectitle = string_of_tag(h4).strip()
            if not sectitle:
                self.log.warn('No section title')
                continue
#            if sectitle == 'Economic and financial indicators':
#                continue
            #self.log.info('Found section: %s' % section_title)
            articles = []
            for tr in section.find_all(tr_has_a_tag):
                article = tr.find('a', href=True)
                title = string_of_tag(article).strip()
                url = article['href']
                if url.startswith('viw'):
                    url = 'http://weekly.chosun.com/client/news/' + url
                    url= url.replace('viw','print', 1)
                    #self.log.info('\tFound article:%s' % title)
                    if url not in urladded:
                        urls.append((sectitle,title,url,None))
                        urladded.add(url)

        if len(urls) == 0:
            self.log.warn('No articles found for WeeklyChosun.')
        return urls
