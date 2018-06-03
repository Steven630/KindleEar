#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook
import re

def getBook():
    return Guardian

class Guardian(BaseFeedBook):
    title                 = 'The Guardian China'
    description           = 'News from the Guardian'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    oldest_article        = 1
#    mastheadfile          = "mh_d5yuansu.gif"
#    coverfile             = "cv_d5yuansu.jpg"
#    network_timeout       = 60
    feeds = [
            ('The Guardian China', 'https://www.theguardian.com/world/china/rss')
#            ('NYT South Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/south-korea/rss.xml'),
#            ('NYT North Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/north-korea/rss.xml'),
           ]
    fulltext_by_readability = False
    keep_image = False
    extra_css      = '''
        figcaption {font-style: italic}
        .gu-image {font-style: italic}
        *[class^="caption"] {font-style: italic}
        .content__standfirst { font-weight: bold; font-size: medium }
        h1 { font-size: large  }
        h2 { font-size: medium  }
        '''
    keep_only_tags = [
#                      dict(name='h1'),
#                      dict(id='content')
                      dict(attrs={'class':['content__headline-standfirst-wrapper','mobile-only','content__main tonal__main tonal__main--tone-feature',
                                           'content__article-body from-content-api js-article__body']}),
                       dict(name='div', attrs={'itemprop':['articleBody']})
#                      dict(id='article-body-blocks')
                     ]
    remove_classes = ['pullquote-paragraph','popup__group-header','hide-on-mobile','control__info',
                      'element element-rich-link element--thumbnail element-rich-link--upgraded',
                      'rich-link tone-news--item ','rich-link tone-news--item','rich-link__container'
                      'personalisation__links','u-h','brand-bar__item brand-bar__item--action','mobile-only footer__primary',
                      'tertiary-navigation','js-mega-nav navigation__expandable','global-navigation js-global-navigation',
                      'popup__group','brand-bar__item--right','main-menu-container',
                      'navigation-group navigation-border secondary-navigation','navigation-group__item','rich-link__title',
                      'submeta','element element-rich-link element--thumbnail element-rich-link--not-upgraded',
                      'rich-link__header','rich-link__title','rich-link__read-more','rich-link__arrow','content__section-label ',
                      'content__section-label','brand-bar__item brand-bar__item--jobs hide-until-tablet hide-on-slim-header',
                      'popup__item brand-bar__popup--jobs','share-modal__content',
                      'content__updated-container content__updated-container--liveblog','content__series-label ','content__series-label',
                      'element element-video fig--has-shares fig--narrow-caption','l-footer u-cf','element element-interactive interactive',
                      'menu-item','menu js-main-menu','subnav','footer__primary mobile-only','meta__social',
                      'content__meta-container js-content-meta js-football-meta u-cf', re.compile('^content__meta-container')
                     ]
    remove_tags_after = [ dict(attrs={'class':[
            'submeta'
    ]})]
    remove_tags_before = [ dict(attrs={'class':[
            'content__section-label__link'
    ]})]
    remove_ids = ['bannerandheader','guardian-services-top-menu']
    
    remove_tags = [{'name':'footer'}, {'name':'aside'}, {'name':'blockquote'},
                   dict(name='a', attrs={'data-link-name':['in standfirst link']}),
                   dict(name=['script', 'noscript', 'style', 'form', 'hr', 'button', 'meta', 'footer','aside','blockquote'])]
