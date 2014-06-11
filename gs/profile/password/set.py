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
from __future__ import absolute_import
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.content.form.base import SiteForm
from .interfaces import ISetPassword, IGSPasswordUser


class SetPasswordForm(SiteForm):
    form_fields = form.Fields(ISetPassword)
    label = u'Change Password'
    pageTemplateFileName = 'browser/templates/set.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, user, request):
        super(SetPasswordForm, self).__init__(user, request)
        self.userInfo = IGSUserInfo(user)

    @form.action(label=u'Change', failure='handle_set_action_failure')
    def handle_set(self, action, data):
        assert self.context
        assert self.form_fields
        assert action
        assert data

        # Using the logged in user, rather than self.context is
        # deliberate. By using the logged in user we prevent anyone from
        # even *accidently* changing the password of another user.
        liu = createObject('groupserver.LoggedInUser', self.context)
        assert not(liu.anonymous), 'Not logged in'
        pu = IGSPasswordUser(liu)
        pu.set_password(data['password1'])

        self.status = u'Your password has been changed.'
        assert type(self.status) == unicode

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'There was an error:'
        else:
            self.status = u'<p>There were errors:</p>'
