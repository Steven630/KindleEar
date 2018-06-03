#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook

def getBook():
    return Chosun

class Chosun(BaseFeedBook):
    title                 = u'朝鲜日报北韩'
    description           = u'朝鲜日报朝鲜新闻'
    language              = 'ko'
    feed_encoding         = "euc-kr"
    page_encoding         = "euc-kr"
    oldest_article        = 1
#    mastheadfile          = "mh_d5yuansu.gif"
#    coverfile             = "cv_d5yuansu.jpg"
#    network_timeout       = 60
    feeds = [
            (u'朝鲜日报北韩', 'http://nk.chosun.com/rss/allArticle.xml')
#            (u'朝鲜主要新闻', 'http://www.feed43.com/nk-topnews.xml')
#            ('NYT North Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/north-korea/rss.xml'),
           ]
    fulltext_by_readability = False
    keep_image = True
    keep_only_tags = [
#                      dict(name='h1'),
                      dict(attrs={'class':['View_Title']}),
                      dict(id='articleBody')
#                       dict(name='div', attrs={'itemprop':['articleBody']})
#                      dict(id='article-body-blocks')
                      ]
    extra_css      = '''
        body { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        p { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        div { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        .par { font-size: 1em;  text-align: justify;  line-height: 1.718em}
        .View_Title { font-size: large  }
        .view_r_caption {font-style: italic}
        '''
