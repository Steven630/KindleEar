#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag

def getBook():
    return EconomistOld


class EconomistOld(BaseFeedBook):
    title                 = 'The Economist Old'
    description           = 'Global news and current affairs from a European perspective, delivered on Friday.'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
    coverfile             = "cv_economist.jpg"
#    coverfile             = get_cover_url(self)
    deliver_days          = ['Friday']
    fulltext_by_readability = False
    keep_image            = True
    
    remove_classes = ['ec-messages', 'dblClkTrk', 'ec-article-info',
                      'share_inline_header', 'related-items','content-image-float clearfix','pullquote',
                      'ec-gallery-carosel','footnotes','yj6qo ajU','ec-active-image','esi-generated pullquote',
                      'ec-topic-widget fullwidth medium','ec-article-info source','blog-post__comments-label',
                      'blog-post__section-date-author','blog-post__foot-note','link-button sections-card__link',
                      'sections-card__list-item','latest-updates-panel__footer latest-updates-panel__footer--blog-post',
                      'latest-updates-panel__label latest-updates-panel__label--blog-post','latest-updates-panel__body',
                      'latest-updates-panel-card__wrapper','latest-updates-panel__article-link','latest-updates-panel-card',
                      'atest-updates-panel-card__body','latest-updates-panel-card__title','latest-updates-panel-card__subtitle',
                      'latest-updates-panel-card__time','blog-post__siblings-list-aside ','blog-post__siblings-list-aside',
                      'blog-post__siblings-list-header ','blog-post__siblings-list-header','special-report-header',
                      'special-report-header-sponser','content_clearfix','column-right'
                      ]
    remove_ids = ['more-kallery']
    remove_tags = [
            dict(name=['script', 'noscript', 'title', 'iframe', 'cf_floatingcontent','object','aside']),
            dict(attrs={'class':['dblClkTrk', 'ec-article-info',
                'share_inline_header', 'related-items','content-image-float clearfix','pullquote','ec-gallery-carosel',
                'footnotes','yj6qo ajU','ec-active-image','esi-generated pullquote','ec-topic-widget fullwidth medium',
                'ec-article-info source','blog-post__comments-label','blog-post__section-date-author','blog-post__foot-note',
                'link-button sections-card__link','sections-card__list-item',
                'latest-updates-panel__footer latest-updates-panel__footer--blog-post',
                'latest-updates-panel__label latest-updates-panel__label--blog-post','latest-updates-panel__body',
                'latest-updates-panel-card__wrapper','latest-updates-panel__article-link','latest-updates-panel-card',
                'atest-updates-panel-card__body','latest-updates-panel-card__title','latest-updates-panel-card__subtitle','latest-updates-panel-card__time']}),
            dict(attrs={'id':['more-kallery']}),
            dict(name='a', attrs={'href':['#footnote1']}),
            {'class': lambda x: x and 'share-links-header' in x},
    ]
    keep_only_tags = [dict(name='hgroup'),dict(name='span', attrs={'class':['location']}),dict(name='article'),dict(id='ec-article-body')]
    remove_tags_after = [ dict(attrs={'class':['blog-post__comments-label']})
    ]
    remove_attributes = ['data-reactid']
    feeds = [
        ('The world this week', 'http://www.economist.com/rss/the_world_this_week_rss.xml'),
        ('Letters', 'http://www.economist.com/rss/letters_rss.xml'),
        ('Leaders', 'http://www.economist.com/rss/leaders_rss.xml'),
        ('Briefings', 'http://www.economist.com/rss/briefings_rss.xml'),
        ('Special reports', 'http://www.economist.com/rss/special_reports_rss.xml'),
        ('Britain', 'http://www.economist.com/rss/britain_rss.xml'),
        ('Europe', 'http://www.economist.com/rss/europe_rss.xml'),
        ('United States', 'http://www.economist.com/rss/united_states_rss.xml'),
        ('The Americas', 'http://www.economist.com/rss/the_americas_rss.xml'),
        ('Middle East and Africa', 'http://www.economist.com/rss/middle_east_and_africa_rss.xml'),
        ('Asia', 'http://www.economist.com/rss/asia_rss.xml'),
        ('China', 'http://www.economist.com/rss/china_rss.xml'),
        ('International', 'http://www.economist.com/rss/international_rss.xml'),
        ('Business', 'http://www.economist.com/rss/business_rss.xml'),
        ('Finance and economics', 'http://www.economist.com/rss/finance_and_economics_rss.xml'),
        ('Science and technology', 'http://www.economist.com/rss/science_and_technology_rss.xml'),
        ('Books and arts', 'http://www.economist.com/rss/books_and_arts_rss.xml'),
        ('Obituary', 'http://www.economist.com/rss/obituary_rss.xml'),
        ]
    
    extra_css= '''
    .headline {font-size: large;}
    .blog-post__rubric { font-weight: bold;  }
    h2 { font-size: medium;  }
    h1 { font-size: medium;  }
    figcaption {font-style: italic}
    .caption {font-style: italic}
    .location { font-size: small;  }
    .xhead { font-weight: bold;  }
    .Bold { font-weight: bold; font-style: normal }
        '''
