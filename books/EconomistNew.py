#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
import urllib

def getBook():
    return TheEconomist
    

def fetch_cover(self):
    mainurl = 'https://www.economist.com/weeklyedition'
    opener = URLOpener(None, timeout=180)
#    opener = URLOpener(self.host, timeout=90)
    result = opener.open(mainurl)
    content = result.content.decode('utf-8')
#    content = result.content.decode(self.feed_encoding)
    soup = BeautifulSoup(content, "lxml")
#    wrapper = soup.find('div', attrs={'class':'print-edition__cover-wrapper'})
    header = soup.find('div', class_='weekly-edition-header__image')
#    div=wrapper.find('div', class_='component-image print-edition__cover-widget__image')
    img = header.find('img', src=True)
    cover = img.get('src')
#    if cover.startswith('/'):
#        cover = 'http://www.economist.com' + cover
    data = urllib.urlopen(cover).read()
    return data

class TheEconomist(BaseFeedBook):
    title                 = 'The Economist Web'
    description           = 'Global news and current affairs from a European perspective, delivered on Friday.'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    mastheadfile          = "mh_economist.gif" 
#    coverfile             = "cv_economist.jpg"
    coverfile             =  fetch_cover
    deliver_days          = ['Friday']
    deliver_times         = [14]
    fulltext_by_readability = False
    keep_image            = True
    needs_subscription    = True
    
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
                      'special-report-header-sponser','content_clearfix','column-right','blog-post__asideable-wrapper',
                      'newsletter-form','blog-post__bottom-panel','share-links-header teaser--wrapped latest-updates-panel__container',
                      'latest-updates-panel__article-link blog-post__section newsletter-form blog-post__bottom-panel',
                      ' latest-updates-panel__article-link blog-post__section newsletter-form blog-post__bottom-panel','related-article',
                      'article__footnote','article__section','ds-share-list','regwall'
                      ]
#    remove_ids = ['more-kallery']
    remove_tags = [
            {'name':'script'},{'name':'noscript'},{'name':'aside'},
            dict(attrs={'aria-label': "Article Teaser"})           
    ]
    keep_only_tags = [{'name':'article'}
                     ]
    remove_tags_after = [ dict(attrs={'class':['blog-post__foot-note','blog-post__comments-label','blog-post__bottom-panel','article__footnote']})
    ]
    remove_attributes = ['data-reactid']
    feeds = [
            ('Index', 'https://www.economist.com/weeklyedition'),
           ]
    
    def ParseFeedUrls(self):
        #return list like [(section,title,url,desc),..]
        login_url = 'https://my.economist.com/'
        main = 'https://www.economist.com/weeklyedition'
#        login_form = {"css-1gytnsx":self.account, "password":self.password}
#        login_response = opener.open(login_url, data=login_form)
#        main = 'https://www.economist.com/'
        urls = []
        urladded = set()
        opener = URLOpener(self.host, timeout=90)
        result = opener.open(main)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
#        content = result.content.decode(self.feed_encoding)
#        soup = BeautifulSoup(content, "lxml")
#        a = soup.find('a', attrs={'class':'latest-printed__cta'})
#        current = a['href']
#        if current.startswith(r'/'):
#            current = 'https://www.economist.com' + url
#        opener = URLOpener(self.host, timeout=90)
#        result = opener.open(current)
#        if result.status_code != 200:
#            self.log.warn('fetch latest edition failed:%s'%main)
#            return []
        content = result.content.decode(self.feed_encoding)
        soup = BeautifulSoup(content, "lxml")
        
        #开始解析
#        for section in soup.find_all('li', attrs={'class':'list__item'}):
#            div = section.find('div')
#            if div is None:
#                self.log.warn('This part skipped.')
#                continue
        thisweek = soup.find('div', class_='layout-weekly-edition-wtw')
        if thisweek:
            h2 = thisweek.find('h2')
            sectitle = string_of_tag(h2).strip()
            if not sectitle:
                self.log.warn('No section title for the world this week')
            for week in thisweek.find_all('a', href=True):
                title = string_of_tag(week).strip()
                url = week['href']
                if url.startswith(r'/'):
                    url = 'https://www.economist.com' + url
                urls.append((sectitle,title,url,None))
        else:
            self.log.warn('The world this week not found.')
                
        for section in soup.find_all(class_= lambda value: value and value.startswith('layout-weekly-edition-section')):
            h2 = section.find('h2')
            sectitle = string_of_tag(h2).strip()
            if not sectitle:
                self.log.warn('No section title')
                continue
            if 'financial indicators' in sectitle:
                continue
            #self.log.info('Found section: %s' % section_title)
#            articles = []
            for node in section.find_all('a', href=True, class_= lambda value: value and value.startswith('headline-link')):
                spans = node.find_all('span')
                if len(spans) == 2: 
                    title = u'{}: {}'.format(*map(string_of_tag, spans))
#            for node in section.find_all('a', href=True):
#                spans = node.findAll('span')
#                if len(spans) == 2:
#                    fly= node.find('span', attrs={'class':'print-edition__link-flytitle'})
#                    pre= string_of_tag(fly).strip()
#                    ti= node.find('span', attrs={'class':'print-edition__link-title'})
#                    post= string_of_tag(ti).strip()
#                    title = pre +': '+ post
                else:
                    title = string_of_tag(node).strip()
                url = node['href']
                if url.startswith(r'/'):
                    url = 'https://www.economist.com' + url
                    #self.log.info('\tFound article:%s' % title)
                if url not in urladded:
                    urls.append((sectitle,title,url,None))
                    urladded.add(url)
                                
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
    
    extra_css= '''
    .flytitle-and-title__flytitle {font-size: medium; font-weight: bold; display: block;}
    .flytitle-and-title__title {font-size: large; font-weight: bold}
    h2 { font-size: medium }
    .blog-post__rubric { font-weight: bold;  }
    figcaption {font-style: italic}
    .caption {font-style: italic}
    .location { font-size: small;  }
    .xhead { font-weight: bold; font-size: medium }
    .Bold { font-weight: bold; font-style: normal }
        '''
