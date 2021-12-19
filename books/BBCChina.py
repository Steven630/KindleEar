#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook
import re

def getBook():
    return BBC

class BBC(BaseFeedBook):
    title                 = 'BBC China'
    description           = 'China News from the BBC'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    oldest_article        = 2
#    mastheadfile          = "mh_d5yuansu.gif"
#    coverfile             = "cv_d5yuansu.jpg"
#    network_timeout       = 60
    feeds = [
             ('BBC China', 'http://feeds.bbci.co.uk/news/world/asia/china/rss.xml')
#            ('NYT South Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/south-korea/rss.xml'),
#            ('NYT North Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/north-korea/rss.xml'),
           ]
    fulltext_by_readability = False
    keep_image = False
    extra_css      = '''
        figcaption {font-style: italic}
        .media-caption__text {font-style: italic}
        .story-body__introduction { font-weight: bold; font-size: medium}
        h2 { font-weight: bold; font-size: medium}
        h1 { font-size: large  }
        '''
    keep_only_tags = [
                      dict(name='h1'),
#                      dict(id='content')
#                      dict(attrs={'class':['story-body']})
                       dict(name='div', attrs={'class':[ re.compile('^ssrcss-uf6wea-RichTextComponentWrapper'),
                                                        'ssrcss-uf6wea-RichTextComponentWrapper e1xue1i86']})
#                      dict(id='article-body-blocks')
                     ]
    remove_classes = ['with-extracted-share-icons','off-screen','story-image-copyright','bbccom_advert bbccom_shut',
                      'bbccom_slot mpu-ad bbccom_standard_slot bbccom_shut','sp-media-asset__smp-message',
                      'sp-media-asset sp-media-asset--lead','player-wrapper','more-wrapper','player-with-placeholder',
                      'tags-container','media-with-caption'
                     ]
    remove_tags_after = [ dict(attrs={'id':[
            'share-tools'
    ]})]
    remove_tags_before = [ dict(attrs={'class':[
            'container'
    ]})]
    remove_ids = ['share-tools']
