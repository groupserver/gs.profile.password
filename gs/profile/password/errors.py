# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
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
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.core import to_ascii
from gs.errormesg.baseerror import BaseErrorPage


class ResetError(BaseErrorPage):
    def __init__(self, context, request):
        super(ResetError, self).__init__(context, request)
        self.resetId = request.form.get('resetId', '')
        self.linkAddress = '%s/r/password/%s' % \
            (self.siteInfo.url, self.resetId)


class ResetIdNotFound(ResetError):
    fileName = 'browser/templates/reset_id_not_found.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        super(ResetIdNotFound, self).__init__(context, request)
        m = 'Hi! I tried resetting my password using the link %s but '\
            'I saw a Password Reset Error page. I tried... but it '\
            'did not help.' % self.linkAddress
        self.message = quote(m)

    def __call__(self, *args, **kw):
        contentType = to_ascii('text/html; charset=UTF-8')
        self.request.response.setHeader(to_ascii('Content-Type'), contentType)
        # Return 404: Not Found
        self.request.response.setStatus(404)
        return self.index(self, *args, **kw)


class ResetIdUsed(ResetError):
    fileName = 'browser/templates/reset_id_used.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        super(ResetIdUsed, self).__init__(context, request)
        m = 'Hi! I tried resetting my password using the link %s but '\
            'I saw a Password Reset Link Used page. I was trying '\
            'to...' % self.linkAddress
        self.message = quote(m)

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        return retval

    def __call__(self, *args, **kw):
        contentType = to_ascii('text/html; charset=UTF-8')
        self.request.response.setHeader(to_ascii('Content-Type'), contentType)
        # Return 410: Gone
        self.request.response.setStatus(410)
        return self.index(self, *args, **kw)


class ResetNoId(BaseErrorPage):
    fileName = 'browser/templates/reset_no_id.pt'
    index = ZopeTwoPageTemplateFile(fileName)

    def __init__(self, context, request):
        super(ResetNoId, self).__init__(context, request)
        self.linkAddress = '%s/r/password/' % self.siteInfo.url
        m = 'Hi! I followed the the link %s but I saw a Password '\
            'Reset Link Error page. I was trying to get to... I found '\
            'the link in...' % self.linkAddress
        self.message = quote(m)

    def __call__(self, *args, **kw):
        contentType = to_ascii('text/html; charset=UTF-8')
        self.request.response.setHeader(to_ascii('Content-Type'), contentType)
        # Return 400: Bad Request
        self.request.response.setStatus(400)
        return self.index(self, *args, **kw)
