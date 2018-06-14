#!/usr/bin/env python
# -*- coding:utf-8 -*-
from base import BaseFeedBook
import re

def getBook():
    return NYTChina

class NYTChina(BaseFeedBook):
    title                 = 'NYT China and Korea'
    description           = 'News from the NYT'
    language              = 'en'
    feed_encoding         = "utf-8"
    page_encoding         = "utf-8"
    oldest_article        = 1
    max_articles_per_feed = 10
#    mastheadfile          = "mh_d5yuansu.gif"
#    coverfile             = "cv_d5yuansu.jpg"
#    network_timeout       = 60
    feeds = [
            ('NYT China', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/china/rss.xml'),
            ('NYT South Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/south-korea/rss.xml'),
            ('NYT North Korea', 'http://www.nytimes.com/svc/collections/v1/publish/www.nytimes.com/topic/destination/north-korea/rss.xml'),
           ]
    fulltext_by_readability = False
    keep_image = False
    extra_css      = '''
        .headline {font-size: large}
        .byline author vcard {font-size: small}
        .story-print-citation {font-size: small}
        .byline-author {font-size: small}
        .byline {font-size: small}
        .date {font-size: small}
        .credit {font-size: small}
        .dateline {font-size: small}  
        .caption {font-style: italic}
        h2 { font-size: medium  }
        h4 { font-size: medium; font-weight: bold }
        h1 { font-size: large  }
        *[class^="ResponsiveMedia-caption"] {font-style: italic}
        *[class^="elementStyles-printInformation"] {font-size: small}
        *[class^="css-1wtlzrm"] {font-style: italic}
        .bottom-of-article {font-size: small}
        '''
#    keep_only_tags = [dict(name='p')]
    remove_tags_after = [ dict(attrs={'class':[
            'module-heading','story-print-citation','story-info','bottom-of-article'
    ]})]
    remove_tags_before = [dict(name=['h1'])]
    remove_ids = ['news-tips-article-promo','player']
    remove_classes = [
            'articleFooter',
            'articleTools',
            'rfd', 'story-footer-links', 'page-footer',
            'columnGroup singleRule',
            'columnGroup last',
            'columnGroup  last',
            'doubleRule',
            'dottedLine',
            'entry-meta',
            'playlist',
            'entry-response module',
            'leftNavTabs',
            'metaFootnote',
            'messages',
            'supported-by hidden nocontent robots-nocontent',
            'sidebar list-view',
            'visually-hidden skip-to-text-link',
            'ad flex-ad nocontent robots-nocontent',
            'accessibility-ad-header visually-hidden',
            'byline-column',
            'story-menu',
            'visually-hidden',
            'bundle-payflow hidden',
            'story-translations',
            'site-index-navigation',
            'menu primary-menu',
            'column',
            'navigation',
            'quick-navigation button-group',
            'content-related-to-video',
            'story-interrupter',
            'newsletter-form',
            'control input-control',
            'footer',
            'reader-satisfaction-survey prompt feedback-prompt story-content hidden',
            'sharetools-label visually-hidden',
            'module trending-module hidden nocontent robots-nocontent',
            'site-index',
            'text-ad bottom-left-ad nocontent robots-nocontent',
            'ad top5-ad hidden nocontent robots-nocontent',
            'module bundle-payflow-module',
            'loader-container',
            'kicker-label',
            'story-notes',
            'story-info',
            'module-heading',
            'newsletter-signup',
            'nocontent robots-nocontent',
            'notification-signup',
            'storage-drawer',
            'inside-story',
            'module box nav',
            'nextArticleLink',
            'nextArticleLink clearfix',
            'post-tools',
            'relatedSearchesModule',
            'side_tool',
            'singleAd',
            'postCategory column',
            'refer tagRefer',  # added for bits blog post
            'entry entry-utility',  # added for DealBook
            'entry-tags',  # added for DealBook
            'footer promos clearfix',  # added for DealBook
            'footer links clearfix',  # added for DealBook
            'tabsContainer',  # added for other blog downloads
            'column lastColumn',  # added for other blog downloads
            'pageHeaderWithLabel',  # added for other gadgetwise downloads
            'column two',  # added for other blog downloads
            'column two last',  # added for other blog downloads
            'column three',  # added for other blog downloads
            'column three last',  # added for other blog downloads
            'column four',  # added for other blog downloads
            'column four last',  # added for other blog downloads
            'column last',  # added for other blog downloads
            'entry entry-related',
            'subNavigation tabContent active',  # caucus blog navigation
            'mediaOverlay slideshow',
            'wideThumb',
            'video',  # added 02-11-2011
            'videoHeader',  # added 02-11-2011
            'articleInlineVideoHolder',  # added 02-11-2011
            'assetCompanionAd',
            'nytint-sectionHeader',
            re.compile('^InlineMessage'),
            re.compile('^RelatedCoverage'),
            re.compile('^styles-translation'),
            re.compile('^SectionBarShare'),
            re.compile('^subNavigation'),
            re.compile('^leaderboard'),
            re.compile('^module'),
            re.compile('commentCount'),
            re.compile('^css-l9vd'),
            re.compile('^ResponsiveAd'),
            re.compile('^styles-shareNetworks'),
            re.compile('^css-30n6iy'),
            re.compile('^ResponsiveMedia-credit'),
            'lede-container',
            'credit',
            'caption-video',
            'interactive promo  layout-large',
            'interactive-image-container', 'interactive-caption',
            'elementStyles-translationLinks--27EiR', 'accessibility-visuallyHidden--OUeHR',
            'Media-credit--1ZFho ResponsiveMedia-credit--3F-q_',
            'SectionBarShare-shareMenu--2ndEi SectionBarShare-toneNews--1a-Gj SectionBarShare-bottom--3ONdV'
    ]
    remove_tags = [
        dict(attrs={'class': [
            'articleFooter',
            'articleTools',
            'rfd', 'story-footer-links', 'page-footer',
            'columnGroup singleRule',
            'columnGroup last',
            'columnGroup  last',
            'doubleRule',
            'dottedLine',
            'entry-meta',
            'entry-response module',
            'leftNavTabs',
            'metaFootnote',
            'messages',
            'supported-by hidden nocontent robots-nocontent',
            'visually-hidden skip-to-text-link',
            'story-interrupter',
            'newsletter-form',
            'control input-control',
            'footer',
            'reader-satisfaction-survey prompt feedback-prompt story-content hidden',
            'sharetools-label visually-hidden',
            'kicker-label',
            'story-notes',
            'story-info',
            'module-heading',
            'newsletter-signup',
            'nocontent robots-nocontent',
            'storage-drawer',
            'inside-story',
            'module box nav',
            'nextArticleLink',
            'nextArticleLink clearfix',
            'post-tools',
            'relatedSearchesModule',
            'side_tool',
            'singleAd',
            'postCategory column',
            'refer tagRefer',  # added for bits blog post
            'entry entry-utility',  # added for DealBook
            'entry-tags',  # added for DealBook
            'footer promos clearfix',  # added for DealBook
            'footer links clearfix',  # added for DealBook
            'tabsContainer',  # added for other blog downloads
            'column lastColumn',  # added for other blog downloads
            'pageHeaderWithLabel',  # added for other gadgetwise downloads
            'column two',  # added for other blog downloads
            'column two last',  # added for other blog downloads
            'column three',  # added for other blog downloads
            'column three last',  # added for other blog downloads
            'column four',  # added for other blog downloads
            'column four last',  # added for other blog downloads
            'column last',  # added for other blog downloads
            'entry entry-related',
            'subNavigation tabContent active',  # caucus blog navigation
            'mediaOverlay slideshow',
            'wideThumb',
            'video',  # added 02-11-2011
            'videoHeader',  # added 02-11-2011
            'articleInlineVideoHolder',  # added 02-11-2011
            'assetCompanionAd',
            'nytint-sectionHeader',
            re.compile('^subNavigation'),
            re.compile('^leaderboard'),
            re.compile('^module'),
            re.compile('commentCount'),
            'lede-container',
            'credit',
            'caption-video'
        ]}),
        dict(
            attrs={'class': lambda x: x and 'related-coverage-marginalia' in x.split()}),
        dict(attrs={'class': lambda x: x and 'hidden' in x.split()}),
        dict(attrs={'class': lambda x: x and 'interactive' in x.split()}),
        dict(attrs={'class': lambda x: x and 'skip-to-text-link' in x.split()}),
        dict(attrs={'class': lambda x: x and 'sharetools' in x.split()}),
        dict(attrs={'class': lambda x: x and 'ad' in x.split()}),
        dict(attrs={'class': lambda x: x and 'visually-hidden' in x.split()}),
        dict(name='div', attrs={'class': re.compile('toolsList')}),  # bits
        dict(name='div', attrs={
             'class': re.compile('postNavigation')}),  # bits
        dict(name='div', attrs={'class': 'tweet'}),
        dict(name='span', attrs={'class': 'commentCount meta'}),
        dict(name='div', attrs={'id': 'header'}),
        # bits, pogue, gadgetwise, open
        dict(name='div', attrs={'id': re.compile('commentsContainer')}),
        # pogue, gadgetwise
        dict(name='ul', attrs={'class': re.compile('entry-tools')}),
        # pogue, gadgetwise
        dict(name='div', attrs={'class': re.compile('nocontent')}),
        dict(name='div', attrs={'id': re.compile('respond')}),  # open
        dict(name='div', attrs={'class': re.compile('entry-tags')}),  # pogue
        dict(name='h4', attrs={'class': 'headline'}),
        dict(id=[
            'adxLeaderboard',
            'pagelinks',
            'adxSponLink',
            'anchoredAd_module',
            'anchoredAd_spot',
            'archive',
            'articleExtras',
            'articleInline',
            'blog_sidebar',
            'businessSearchBar',
            'cCol',
            'entertainmentSearchBar',
            'footer',
            'header',
            'header_search',
            'inlineBox',
            'login',
            'masthead',
            'masthead-nav',
            'masthead-social',
            'memberTools',
            'navigation', 'navigation-ghost', 'navigation-modal', 'navigation-edge',
            'page-footer',
            'portfolioInline',
            'readerReviews',
            'readerReviewsCount',
            'relatedArticles',
            'relatedTopics',
            'respond',
            'ribbon',
            'side_search',
            'side_index',
            'side_tool',
            'toolsRight',
            'skybox',  # added for DealBook
            'TopAd',  # added for DealBook
            'related-content',  # added for DealBook
            'whats-next',
            'newsletter-promo',
        ]),
        dict(name=['script', 'noscript', 'style', 'form', 'hr', 'button', 'meta', 'footer']),
        dict(name='span', string='image')
    ]
