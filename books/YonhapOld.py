#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook

def getBook():
    return Yonhap

class Yonhap(BaseFeedBook):
    title                 = u'韩联社朝鲜'
    description           = u'朝鲜新闻'
    language              = 'ko'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8-sig"
    oldest_article        = 1
    mastheadfile          = "mh_d5yuansu.gif"
    coverfile             = "cv_d5yuansu.jpg"
#    network_timeout       = 60
    feeds = [
            (u'韩联社朝鲜', 'http://www.feed43.com/yonhap_nkportal.xml'),
            (u'朝鲜主要新闻', 'http://www.feed43.com/nk-topnews.xml')
#            ('NYT North Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/north-korea/rss.xml'),
           ]
    fulltext_by_readability = False
    keep_image = True
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
                      'img-info'
                     ]
    remove_tags_after = [ dict(attrs={'class':[
            'pblsh'
    ]})]
