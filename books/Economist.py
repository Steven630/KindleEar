#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import urllib

def getBook():
    return TheEconomist
    

def fetch_cover(self):
    mainurl = 'http://www.economist.com/printedition'
    opener = URLOpener(None, timeout=90)
#    opener = URLOpener(self.host, timeout=90)
    result = opener.open(mainurl)
    content = result.content.decode('utf-8')
#    content = result.content.decode(self.feed_encoding)
    soup = BeautifulSoup(content, "lxml")
    div=soup.find('div', attrs={'class':'print-edition__cover-widget'})
    img = div.find('img', src=True)
    cover = img.get('src')
    if cover.startswith('/'):
        cover = 'http://www.economist.com' + cover
    data = urllib.urlopen(cover).read()
    return data

class TheEconomist(BaseFeedBook):
    title                 = 'The Economist RSS'
    description           = 'Global news and current affairs from a European perspective, delivered on Friday.'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
#    coverfile             = "cv_economist.jpg"
    coverfile             =  fetch_cover
    deliver_days          = ['Friday']
    deliver_times         = [18]
    fulltext_by_readability = False
    keep_image            = True
    
    remove_classes = ['ec-messages', 'dblClkTrk', 'ec-article-info',
                      'share_inline_header', 'related-items','pullquote','ad-panel__googlead'
                      'ec-gallery-carosel','footnotes','yj6qo ajU','esi-generated pullquote',
                      'ec-topic-widget fullwidth medium','ec-article-info source','blog-post__comments-label',
                      'blog-post__section-date-author','blog-post__foot-note','link-button sections-card__link',
                      'sections-card__list-item','latest-updates-panel__footer latest-updates-panel__footer--blog-post',
                      'latest-updates-panel__label latest-updates-panel__label--blog-post','latest-updates-panel__body',
                      'latest-updates-panel-card__wrapper','latest-updates-panel__article-link','latest-updates-panel-card',
                      'atest-updates-panel-card__body','latest-updates-panel-card__title','latest-updates-panel-card__subtitle',
                      'latest-updates-panel-card__time','blog-post__siblings-list-aside ','blog-post__siblings-list-aside',
                      'blog-post__siblings-list-header ','blog-post__siblings-list-header','special-report-header',
                      'special-report-header-sponser','content_clearfix','column-right','blog-post__asideable-wrapper'
                      ]
#    remove_ids = ['more-kallery']
    remove_tags = [
            {'name':'script'},{'name':'noscript'},{'name':'aside'}
    ]
    keep_only_tags = [{'name':'article'}
                     ]
    remove_tags_after = [ dict(attrs={'class':['blog-post__foot-note','blog-post__comments-label']})
    ]
    remove_attributes = ['data-reactid']
    feeds = [
        ('The world this week', 'http://www.economist.com/rss/the_world_this_week_rss.xml'),
        ('Letters', 'http://www.economist.com/feeds/print-sections/68/letters.xml'),
        ('Leaders', 'http://www.economist.com/feeds/print-sections/69/leaders.xml'),
        ('Briefings', 'http://www.economist.com/feeds/print-sections/102/briefings2.xml'),
        ('Briefings', 'http://www.economist.com/feeds/print-sections/104/briefings1.xml'),
        ('Technology Quarterly', 'http://www.economist.com/feeds/print-sections/90/technology-quarterly.xml'),
        ('Christmas Specials', 'http://www.economist.com/feeds/print-sections/91/christmas-specials.xml'),
        ('Special reports', 'http://www.economist.com/feeds/print-sections/103/special-reports.xml'),
        ('Britain', 'http://www.economist.com/feeds/print-sections/76/britain.xml'),
        ('Europe', 'http://www.economist.com/feeds/print-sections/75/europe.xml'),
        ('United States', 'http://www.economist.com/feeds/print-sections/71/united-states.xml'),
        ('The Americas', 'http://www.economist.com/feeds/print-sections/72/the-americas.xml'),
        ('Middle East and Africa', 'http://www.economist.com/feeds/print-sections/99/middle-east-africa.xml'),
        ('Asia', 'http://www.economist.com/feeds/print-sections/73/asia.xml'),
        ('China', 'http://www.economist.com/feeds/print-sections/77729/china.xml'),
        ('International', 'http://www.economist.com/feeds/print-sections/74/international.xml'),
        ('Business', 'http://www.economist.com/feeds/print-sections/77/business.xml'),
        ('Finance and economics', 'http://www.economist.com/feeds/print-sections/79/finance-and-economics.xml'),
        ('Science and technology', 'http://www.economist.com/feeds/print-sections/80/science-and-technology.xml'),
        ('Books and arts', 'http://www.economist.com/feeds/print-sections/89/books-and-arts.xml'),
        ('Obituary', 'http://www.economist.com/feeds/print-sections/82/obituary.xml'),
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

#    def preprocess_raw_html(self, raw, url):
#        soup = self.index_to_soup(raw)
#        for div in soup.findAll(**classes('lazy-image')):
#            noscript = div.find('noscript')
#            img = noscript.find('img')
#            noscript.replaceWith(img)
#        return type(u'')(soup)

