#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
from base import BaseFeedBook

def getBook():
    return DongaEdi

class DongaEdi(BaseFeedBook):
    title                 = u'东亚日报每日社论'
    description           = u'东亚日报每日社论'
    language              = 'ko'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_ftchinese.gif"
    coverfile             = "cv_ftchinese.jpg"
    oldest_article        = 1
    fulltext_by_readability = False
    
    feeds = [
            (u'동아일보 오피니언', 'http://rss.donga.com/editorials.xml'),
            ]

    keep_only_tags = [
#                      dict(name='h1'),
#                      dict(id='articleWrap'),
#                      dict(attrs={'class':['article-wrap article-wrap2 article-font3','article-wrap']})
                       dict(name='div', attrs={'class': 'newsView' })
#                      dict(id='article-body-blocks')
                     ]
    extra_css      = '''
        body { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        p { font-size: 1em;  text-align: justify;  line-height: 1.718em }
        div { font-size: 1em;  text-align: justify;  line-height: 1.718em }
        h1 { font-size: large  }
        h2 { font-size: medium; font-weight: bold }
        .ex {font-style: italic}
        '''
    remove_classes = ['etc']
    
    def fetcharticle(self, url, opener, decoder):
        m = re.search(r'/(\d{8})/(\d{8,})', url)
        if m:
            pubdate=m.group(1)
            artnum=m.group(2)
            url = 'http://news.donga.com/View?gid=' + artnum +'&date=' + pubdate
        return BaseFeedBook.fetcharticle(self,url,opener,decoder)
