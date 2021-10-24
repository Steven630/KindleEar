#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook

def getBook():
    return TheEconomist
    

class TheEconomist(BaseFeedBook):
    title                 = 'The Economist Fulltext RSS'
    description           = 'Global news and current affairs from a European perspective, delivered on Friday.'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
#    coverfile             =  fetch_cover
    deliver_days          = ['Friday']
    deliver_times         = [14]
    fulltext_by_readability = False
    keep_image            = True
    

    feeds = [
        ('The Economist', 'https://feedx.net/rss/economistp.xml')
        ]
    
    extra_css= '''
    .flytitle-and-title__flytitle {font-size: large; font-weight: bold}
    .flytitle-and-title__title {font-size: large; font-weight: bold}
    .blog-post__rubric { font-weight: bold;  }
    figcaption {font-style: italic}
    .caption {font-style: italic}
    .location { font-size: small;  }
    .xhead { font-weight: bold;  }
    .Bold { font-weight: bold; font-style: normal }
        '''
