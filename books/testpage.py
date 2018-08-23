from base import URLOpener
import urllib

def debug_mail(content, name='page.html'):
    from google.appengine.api import mail
    mail.send_mail(SRC_EMAIL, SRC_EMAIL, "KindleEar Debug", "KindlerEar",
    attachments=[(name, content),])

def debug_fetch(url, name='page.html'):
    if not name:
        name = 'page.html'
    opener = URLOpener()
    result = opener.open(url)
    if result.status_code == 200 and result.content:
        debug_mail(result.content, name)

testresult = debug_fetch('https://www.economist.com/printedition/', name='page.html')
debug_mail(testresult, name='page.html')
