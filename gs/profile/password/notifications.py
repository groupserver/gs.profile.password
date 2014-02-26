# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import unicode_literals
from urllib import quote
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import SiteEmail, TextMixin
from gs.profile.base.page import ProfilePage
UTF8 = 'utf-8'


class ResetMessage(SiteEmail, ProfilePage):
    subject = 'Password reset'

    @Lazy
    def supportEmail(self):
        m = 'Hello,\n\nI recieved a password-reset message for my profile '\
            'at\n    {0}/{1}\nand...'
        msg = m.format(self.siteInfo.url, self.userInfo.url)
        sub = quote(self.subject)
        url = 'mailto:{0}?Subject={1}&body={2}'
        retval = url.format(self.siteInfo.get_support_email(), sub,
                            quote(msg.encode(UTF8)))
        return retval


class ResetMessageText(ResetMessage, TextMixin):
    def __init__(self, context, request):
        super(ResetMessageText, self).__init__(context, request)
        filename = 'gs-profile-password-reset-{0}.txt'.format(self.userInfo.id)
        self.set_header(filename)
