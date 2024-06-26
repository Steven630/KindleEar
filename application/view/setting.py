#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#设置页面
import locale, os, textwrap
from flask import Blueprint, render_template, request, redirect, session
from flask import current_app as app
from flask_babel import gettext as _
from ..base_handler import *
from ..utils import str_to_bool, str_to_int, ke_encrypt
from ..back_end.db_models import *
from ..back_end.send_mail_adpt import avaliable_sm_services, send_mail
from .subscribe import UpdateBookedCustomRss

bpSetting = Blueprint('bpSetting', __name__)

supported_languages = ['zh', 'tr_TR', 'en']

all_timezones = {'UTC-12:00': -12, 'UTC-11:00': -11, 'UTC-10:00': -10, 'UTC-9:30': -9.5,
    'UTC-9:00': -9, 'UTC-8:00': -8, 'UTC-7:00': -7, 'UTC-6:00': -6, 'UTC-5:00': -5,
    'UTC-4:00': -4, 'UTC-3:30': -3.5, 'UTC-3:00': -3, 'UTC-2:00': -2, 'UTC-1:00': -1,
    'UTC': 0, 'UTC+1:00': 1, 'UTC+2:00': 2, 'UTC+3:00': 3, 'UTC+3:30': 3.5,
    'UTC+4:00': 4, 'UTC+4:30': 4.5, 'UTC+5:00': 5, 'UTC+5:30': 5.5, 'UTC+5:45': 5.75, 
    'UTC+6:00': 6, 'UTC+6:30': 6.5, 'UTC+7:00': 7, 'UTC+8:00': 8, 'UTC+8:45': 8.75, 
    'UTC+9:00': 9, 'UTC+9:30': 9.5, 'UTC+10:00': 10, 'UTC+10:30': 10.5, 'UTC+11:00': 11,
    'UTC+12:00': 12, 'UTC+12:45': 12.75, 'UTC+13:00': 13, 'UTC+14:00': 14}

@bpSetting.route("/setting", endpoint='Setting')
@login_required()
def Setting(tips=None):
    user = get_login_user()
    sm_services = avaliable_sm_services()
    return render_template('setting.html', tab='set', user=user, tips=tips, langMap=LangMap(), 
        sm_services=sm_services, all_timezones=all_timezones)

@bpSetting.post("/setting", endpoint='SettingPost')
@login_required()
def SettingPost():
    user = get_login_user()
    form = request.form
    keMail = form.get('kindle_email', '').strip(';, ')
    myTitle = form.get('rss_title')

    #service==admin 说明和管理员的设置一致
    sm_srv_need = False
    sm_srv_type = ''
    if user.name == os.getenv('ADMIN_NAME') or user.send_mail_service.get('service') != 'admin':
        sm_srv_need = True
        sm_srv_type = form.get('sm_service')
        sm_apikey = form.get('sm_apikey', '')
        sm_secret_key = form.get('sm_secret_key', '')
        sm_host = form.get('sm_host', '')
        sm_port = str_to_int(form.get('sm_port'))
        sm_username = form.get('sm_username', '')
        sm_password = form.get('sm_password', '')
        sm_save_path = form.get('sm_save_path', '')
        send_mail_service = {'service': sm_srv_type, 'apikey': sm_apikey, 'secret_key': sm_secret_key,
            'host': sm_host, 'port': sm_port, 'username': sm_username, 'password': '', 
            'save_path': sm_save_path}
        #只有处于smtp模式并且密码存在才更新，空或几个星号则不更新
        if sm_srv_type == 'smtp':
            if sm_password and sm_password.strip('*'):
                send_mail_service['password'] = user.encrypt(sm_password)
            else:
                send_mail_service['password'] = user.send_mail_service.get('password', '')
    
    if not keMail:
        tips = _("Kindle E-mail is requied!")
    elif not myTitle:
        tips = _("Title is requied!")
    elif sm_srv_type == 'sendgrid' and not sm_apikey:
        tips = _("Some parameters are missing or wrong.")
    elif sm_srv_type == 'smtp' and not all((sm_host, sm_port, sm_password)):
        tips = _("Some parameters are missing or wrong.")
    elif sm_srv_type == 'local' and not sm_save_path:
        tips = _("Some parameters are missing or wrong.")
    else:
        base_config = user.base_config
        book_config = user.book_config

        enable_send = form.get('enable_send')
        base_config['enable_send'] = enable_send if enable_send in ('all', 'recipes') else ''
        base_config['kindle_email'] = keMail
        base_config['timezone'] = float(form.get('timezone', '0'))
        user.send_time = int(form.get('send_time', '0'))
        book_config['type'] = form.get('book_type', 'epub')
        book_config['device'] = form.get('device_type', 'kindle')
        book_config['title_fmt'] = form.get('title_fmt', '')
        allDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        user.send_days = [weekday for weekday, day in enumerate(allDays) if str_to_bool(form.get(day, ''))]
        book_config['mode'] = form.get('book_mode', '')
        book_config['rm_links'] = form.get('remove_hyperlinks', '')
        book_config['author_fmt'] = form.get('author_format', '') #修正Kindle 5.9.x固件的bug【将作者显示为日期】
        book_config['title'] = myTitle
        book_config['language'] = form.get("book_language", "en")
        book_config['oldest_article'] = int(form.get('oldest', 7))
        book_config['time_fmt'] = form.get('time_fmt', '')
        user.base_config = base_config
        user.book_config = book_config
        if sm_srv_need:
            user.send_mail_service = send_mail_service
        user.save()
        tips = _("Settings Saved!")

        #根据自定义RSS的使能设置，将自定义RSS添加进订阅列表或从订阅列表移除
        UpdateBookedCustomRss(user)
    
    sm_services = avaliable_sm_services()
    return render_template('setting.html', tab='set', user=user, tips=tips, langMap=LangMap(), 
        sm_services=sm_services, all_timezones=all_timezones)

@bpSetting.post("/send_test_email", endpoint='SendTestEmailPost')
@login_required()
def SendTestEmailPost():
    user = get_login_user()
    srcUrl = request.form.get('url', '')
    body = textwrap.dedent(f"""\
    Dear {user.name}, 

    This is a test email from KindleEar, sent to verify the accuracy of the email sending configuration.  
    Please do not reply it.   

    Receiving this email confirms that your KindleEar web application can send emails successfully.   
    Thank you for your attention to this matter.   

    Best regards,
    [KindleEar]
    [From {srcUrl}]
    """)

    emails = user.cfg('kindle_email').split(',') if user.cfg('kindle_email') else []
    userEmail = user.cfg('email')
    if userEmail and userEmail not in emails:
        emails.append(userEmail)
    
    if emails:
        status = 'ok'
        try:
            send_mail(user, emails, 'Test email from KindleEar', body, attachments=[('test.txt', body.encode('utf-8'))])
        except Exception as e:
            status = str(e)
    else:
        status = _("You have not yet set up your email address. Please go to the 'Admin' page to add your email address firstly.")

    return {'status': status, 'emails': emails}

#显示环境变量的值
@bpSetting.route('/env')
@login_required()
def DisplayEnv():
    strEnv = []
    for d in os.environ:
        strEnv.append("<pre><p>" + str(d).rjust(28) + " | " + str(os.environ[d]) + "</p></pre>")
    strEnv.append("<pre><p>" + 'appDir'.rjust(28) + " | " + appDir + "</p></pre>")
    return ''.join(strEnv)

#设置国际化语种
@bpSetting.route("/setlocale/<langCode>")
def SetLang(langCode):
    global supported_languages
    if langCode not in supported_languages:
        langCode = "en"
    session['langCode'] = langCode
    url = request.args.get('next', '/')
    return redirect(url)

#Babel选择显示哪种语言的回调函数
def get_locale():
    try:
        langCode = session.get('langCode')
    except: #Working outside of request context
        langCode = 'en'
    return langCode if langCode else request.accept_languages.best_match(supported_languages)

#各种语言的语种代码和文字描述的对应关系
def LangMap():
    return {"zh-cn": _("Chinese"),
        "en-us": _("English"),
        "fr-fr": _("French"),
        "es-es": _("Spanish"),
        "pt-br": _("Portuguese"),
        "de-de": _("German"),
        "it-it": _("Italian"),
        "ja-jp": _("Japanese"),
        "ru-ru": _("Russian"),
        "tr-tr": _("Turkish"),
        "ko-kr": _("Korean"),
        "ar": _("Arabic"),
        "cs": _("Czech"),
        "nl": _("Dutch"),
        "el": _("Greek"),
        "hi": _("Hindi"),
        "ms": _("Malaysian"),
        "bn": _("Bengali"),
        "fa": _("Persian"),
        "ur": _("Urdu"),
        "sw": _("Swahili"),
        "vi": _("Vietnamese"),
        "pa": _("Punjabi"),
        "jv": _("Javanese"),
        "tl": _("Tagalog"),
        "ha": _("Hausa"),}
