#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#一些常用工具函数

import os, sys, hashlib, base64, secrets, datetime, re
from urllib.parse import urlparse

#比较安全的eval
#txt: 需要编译的字符串
#gbl: 全局字典
#local: 本地字典
def safe_eval(txt, gbl=None, local=None):
    gbl = gbl or {}
    local = local or {}
    code = compile(txt, '<user input>', 'eval')
    reason = None
    banned = ('eval', 'compile', 'exec', 'getattr', 'hasattr', 'setattr', 'delattr',
        'classmethod', 'globals', 'help', 'input', 'isinstance', 'issubclass', 'locals',
        'open', 'print', 'property', 'staticmethod', 'vars', 'os')
    for name in code.co_names:
        if re.search(r'^__\S*__$', name):
            reason = 'dunder attributes not allowed' # pragma: no cover
        elif name in banned:
            reason = 'arbitrary code execution not allowed' # pragma: no cover
        if reason:
            raise NameError(f'{name} not allowed : {reason}') # pragma: no cover
    return eval(code, gbl, local)

#当异常出现时，使用此函数返回真实引发异常的文件名，函数名和行号
def get_exc_location():
    #追踪到最终的异常引发点
    exc_info = sys.exc_info()[2]
    last_exc = exc_info.tb_next
    while (last_exc.tb_next):
        last_exc = last_exc.tb_next
    fileName = os.path.basename(last_exc.tb_frame.f_code.co_filename)
    funcName = last_exc.tb_frame.f_code.co_name
    lineNo = last_exc.tb_frame.f_lineno
    last_exc = None
    exc_info = None
    return fileName, funcName, lineNo

#字符串转整数，出错则返回0
def str_to_int(txt, default=0):
    try:
        return int(txt.split('.')[0].replace(',', '').strip())
    except:
        return default

#字符串转bool(txt)
def str_to_bool(txt):
    return str(txt or '').lower().strip() in ('yes', 'true', 'on', 'enable', 'enabled', '1', 'checked')

#返回字符串格式化时间
def time_str(fmt="%Y-%m-%d %H:%M", tz=0):
    return tz_now(tz).strftime(fmt)

#返回datetime实例，包含timezone信息
def tz_now(tz=0):
    return datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=tz)))

#隐藏真实email地址，使用星号代替部分字符
#输入单个email字符串或列表，返回部分隐藏的字符串
def hide_email(email):
    emailList = [email] if isinstance(email, str) else email
    newEmails = []
    for item in emailList:
        if '@' not in item:
            newEmails.append(item)
            continue

        item = item.split('@')
        if len(item[0]) < 4:
            return item[0][0] + '**@' + item[-1]
        to = item[0][0] + '*****' + item[0][-1]
        newEmails.append(to + '@' + item[-1])
    if not newEmails:
        return email
    elif len(newEmails) == 1:
        return newEmails[0]
    else:
        return newEmails

#隐藏真实的网址
def hide_website(site):
    if not site:
        return ''
        
    parts = urlparse(site)
    path = parts.path if parts.path else parts.netloc
    if '.' in path:
        pathArray = path.split('.')
        if len(pathArray[0]) > 4:
            pathArray[0] = pathArray[0][:2] + '**' + pathArray[0][-1]
        else:
            pathArray[0] = pathArray[0][0] + '**'
            pathArray[1] = pathArray[1][0] + '**'
        site = '.'.join(pathArray)
    elif len(path) > 4:
        site = path[:2] + '**' + path[-1]
    else:
        site = path[0] + '**'
    return site

#判断url是否合法
def url_validator(url):
    try:
        parts = urlparse(url)
        return all([parts.scheme, parts.netloc])
    except AttributeError:
        return False

#将字节长度转换为人类友好的字符串，比如 2000 -> 2kB
#value: 字节长度
#binary: 进位是2进制还是10进制
#suffix: 字符串后缀
def filesizeformat(value, binary=False, suffix='B'):
    value = abs(float(value))
    if binary:
        base = 1024
        prefixes = ('', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi')
    else:
        base = 1000
        prefixes = ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')

    for unit in prefixes:
        if value < base:
            return f"{value:3.1f} {unit}{suffix}" if unit else f"{int(value)} {suffix}"
        value /= base
    return f"{value:.1f} {unit}{suffix}"


#将字符串安全转义到xml格式，有标准库函数xml.sax.saxutils.escape()，但是简单的功能就简单的函数就好
def xml_escape(txt):
    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    txt = txt.replace(">", "&gt;")
    txt = txt.replace('"', "&quot;")
    txt = txt.replace("'", "&apos;")
    return txt

def xml_unescape(txt):
    txt = txt.replace("&amp;", "&")
    txt = txt.replace("&lt;", "<")
    txt = txt.replace("&gt;", ">")
    txt = txt.replace("&quot;", '"')
    txt = txt.replace("&apos;", "'")
    return txt

#-----------以下几个函数为安全相关的
def new_secret_key(length=12):
    allchars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXZYabcdefghijklmnopqrstuvwxyz'
    return ''.join([secrets.choice(allchars) for i in range(length)])

def ke_encrypt(txt: str, key: str):
    return _ke_auth_code(txt, key, 'encode')
    
def ke_decrypt(txt: str, key: str):
    return _ke_auth_code(txt, key, 'decode')

def _ke_auth_code(txt: str, key: str, act: str='decode'):
    if not txt:
        return ''
        
    key = key or ''
    key = hashlib.md5(key.encode('utf-8')).hexdigest()
    keyA = hashlib.md5(key[:16].encode('utf-8')).hexdigest()
    keyB = hashlib.md5(key[16:].encode('utf-8')).hexdigest()
    cryptKey = keyA + hashlib.md5(keyA.encode('utf-8')).hexdigest()
    keyLength = len(cryptKey)
    
    if act == 'decode':
        try:
            txt = base64.urlsafe_b64decode(txt).decode('utf-8')
        except:
            txt = ''
    else:
        txt = hashlib.md5((txt + keyB).encode('utf-8')).hexdigest()[:16] + txt
    stringLength = len(txt)
    
    result = ''
    box = list(range(256))
    rndkey = {}
    for i in range(256):
        rndkey[i] = ord(cryptKey[i % keyLength])
    
    j = 0
    for i in range(256):
        j = (j + box[i] + rndkey[i]) % 256
        tmp = box[i]
        box[i] = box[j]
        box[j] = tmp
    a = j = 0
    for i in range(stringLength):
        a = (a + 1) % 256
        j = (j + box[a]) % 256
        tmp = box[a]
        box[a] = box[j]
        box[j] = tmp
        result += chr(ord(txt[i]) ^ (box[(box[a] + box[j]) % 256]))

    if act == 'decode':
        if result[:16] == hashlib.md5((result[16:] + keyB).encode('utf-8')).hexdigest()[:16]:
            return result[16:]
        else:
            return ''
    else:
        return base64.urlsafe_b64encode(result.encode('utf-8')).decode('utf-8')
