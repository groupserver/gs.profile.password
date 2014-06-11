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
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from gs.profile.notify.sender import MessageSender


class ResetNotifier(object):
    textTemplateName = 'gs-profile-password-reset-message.txt'
    htmlTemplateName = 'gs-profile-password-reset-message.html'

    def __init__(self, user, request):
        self.context = self.user = user
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h if h else 'text/html')

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                    name=self.htmlTemplateName)
        assert retval
        return retval

    def notify(self, siteInfo, userInfo, resetLink, toAddr):
        s = 'Password reset at {0} (action required)'
        subject = s.format(siteInfo.name)
        text = self.textTemplate(userInfo=userInfo, resetLink=resetLink)
        html = self.htmlTemplate(userInfo=userInfo, resetLink=resetLink)
        ms = MessageSender(self.context, userInfo)
        ms.send_message(subject, text, html, toAddresses=[toAddr])
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        self.oldContentType)
