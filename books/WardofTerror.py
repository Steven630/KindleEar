#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook

def getBook():
    return WeixinRss

class WeixinRss(BaseFeedBook):
    title                 = u'微信'
    description           = u'微信RSS'
    language              = 'zh-cn'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_ftchinese.gif"
    coverfile             = "cv_ftchinese.jpg"
    oldest_article        = 3
    
    feeds = [
            (u'微信', 'https://werss.app/api/v1/xfeeds/c74ada88-6a8b-4317-8fdf-8335436f8f27.xml', True),
            ]

    keep_image = False
