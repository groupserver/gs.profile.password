# -*- coding: utf-8 -*-
from textwrap import TextWrapper
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart

utf8 = 'utf-8'


def create_reset_message(userInfo, siteInfo, toAddr, fromAddr, resetId):
    container = MIMEMultipart('alternative')
    subject = u'Reset Password on %s' % siteInfo.name
    container['Subject'] = str(Header(subject.encode(utf8), utf8))
    container['From'] = str(fromAddr)
    container['To'] = str(toAddr)

    wrapper = TextWrapper(width=72)
    b = 'We received a request to reset your password at %s. '\
        'All you have to do is set a new password. To do this, '\
        'please click the following link.' % siteInfo.name
    body = '\n'.join(wrapper.wrap(b))

    u = '%s/r/password/%s' % (siteInfo.url, resetId)
    d = {
        'userName': userInfo.name,
        'siteName': siteInfo.name,
        'siteUrl': siteInfo.url,
        'body': body,
        'resetUrl': u
    }

    t = u'''Hi %(userName)s,

%(body)s
  %(resetUrl)s

--
%(siteName)s
%(siteUrl)s
''' % d
    text = MIMEText(t.strip().encode(utf8), 'plain', utf8)
    container.attach(text)

    h = u'''<p><strong>Hi %(userName)s,</strong></p>

<p>%(body)s</p>
<pre>
  <a href="%(resetUrl)s">%(resetUrl)s</a>
</pre>
<hr/>
<p><a href="%(siteUrl)s">%(siteName)s</a></p>
''' % d
    html = MIMEText(h.encode(utf8), 'html', utf8)
    container.attach(html)

    retval = container.as_string()
    assert retval
    assert type(retval) == str
    return retval
