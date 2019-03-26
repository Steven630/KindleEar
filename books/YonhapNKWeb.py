#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return YonhapNK
    

class YonhapNK(BaseFeedBook):
    title                 =  u'韩联社朝鲜要闻（网页）'
    description           =  u'朝鲜新闻'
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
        main = 'https://www.yna.co.kr/nk/index'
        urls = []
        urladded = set()
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch mainnews failed:%s'%main)
            
        content = result.content.decode(self.page_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
        section = soup.find('section', attrs={'class':'column-type01 column-newslist'})
        for article in section.find_all('article'):
            if article is None:
                self.log.warn('This article not found')
                continue
            h2 = article.find('h2')
            a = h2.find('a', href=True)
            atitle = string_of_tag(a).strip()
            url = a['href']
            if url.startswith('/'):
                url='https:'+ url
            elif url.startswith('HTTP'):
                url=url.replace('HTTP','http')
            if url not in urladded:
                urls.append((u'韩联社朝鲜要闻',atitle,url,None))
                urladded.add(url)
            related = article.find('div', attrs={'class':'v-related'})
            if related:
                span = related.find('span')
                if span:
                    relateda = span.find('a', href=True)
                    rtitle = string_of_tag(relateda).strip()
                    rtitle = 'Related: '+ rtitle #在相关文章标题前加标志
                    rurl = relateda['href']
                    if rurl.startswith('/'):
                        rurl= 'https:'+ rurl
                    elif rurl.startswith('HTTP'):
                        rurl=rurl.replace('HTTP','http')
                    if rurl not in urladded:
                        urls.append((u'韩联社朝鲜要闻',rtitle,rurl,None))
                        urladded.add(rurl)
                        
        part2 = 'https://www.yna.co.kr/nk/news/all'
        opener2 = URLOpener(self.host, timeout=90)
        result2 = opener2.open(part2)
        if result2.status_code != 200:
            self.log.warn('fetch latest news failed:%s'%main)
        content2 = result2.content.decode(self.page_encoding)
        soup2 = BeautifulSoup(content2, "lxml")
        sect = soup2.find('ul', attrs={'class':'list-type01 yna-more'})
        for arti in sect.find_all('article'):
            h = arti.find('h2')
            a2 = h.find('a', href=True)
            title = string_of_tag(a2).strip()
            if u'[북한날씨]' in title:
                continue
            aurl = a2['href']
            if aurl.startswith('/'):
                aurl= 'https:'+ aurl
            elif aurl.startswith('HTTP'):
                aurl=aurl.replace('HTTP','http')
            if aurl not in urladded:
                urls.append((u'朝鲜最新消息',title,aurl,None))
                urladded.add(aurl)             
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
