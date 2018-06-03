#!/usr/bin/env python
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from base import BaseFeedBook, URLOpener, string_of_tag
from lib.autodecoder import AutoDecoder

def getBook():
    return OctoberMag

class OctoberMag(BaseFeedBook):
    title               = u'十月（模仿）'
    description         = u'十月（模仿）'
    __author__          = 'Steven630'
    language            = 'zh-cn'
    feed_encoding       = "GB18030"
    page_encoding       = "GB18030"
    mastheadfile        = "mh_nfzm.gif"
    coverfile           = "cv_nfzm.jpg"
    deliver_days        = ['Friday']
    needs_subscription  = True

    def ParseFeedUrls(self):
        login_url = "http://bbstsg.vip.qikan.com/Login.aspx"
        content_url = "http://bbstsg.vip.qikan.com/text/Mag.aspx?issn=ACB37AEA-8FB7-4855-B7CA-D228E972162F"
        urls = []
        opener = URLOpener(self.host, timeout=60)
        login_form = {"ctl00$ContentPlaceHolder1$txtUserName":self.account, "ctl00$ContentPlaceHolder1$txtPassword":self.password}
        login_response = opener.open(login_url, data=login_form)
        result = opener.open(content_url)
        if result.status_code != 200:
            self.log.warn('fetch webpage failed:%s'%main)
            return []
        if self.feed_encoding:
            try:
                content = result.content.decode(self.feed_encoding)
            except UnicodeDecodeError:
                content = AutoDecoder(False).decode(result.content,opener.realurl,result.headers)
        else:
            content = AutoDecoder(False).decode(result.content,opener.realurl,result.headers)
        soup = BeautifulSoup(content, "lxml")
        for section in soup.find_all('dl'):
            dt=section.find('dt')
            span=dt.find('span')
            if span:
                sectitle = string_of_tag(span).strip()
            for dd in section.find_all('dd'):
                a=dd.find('a', href=True)
                title = string_of_tag(a).strip()
                url = a['href']
                if url.startswith('Article'):
                    url = 'http://bbstsg.vip.qikan.com/text/'+url
                urls.append((sectitle,title,url,None))
        if len(urls) == 0:
            self.log.warn('len of urls is zero.')
        return urls
