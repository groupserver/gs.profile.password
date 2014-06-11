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
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.content.form.base import SiteForm
from gs.core import to_id
from gs.profile.email.base.emailaddress import address_exists
from Products.CustomUserFolder.interfaces import IGSUserInfo
from .audit import Auditor, REQUEST, REQUEST_FAIL
from .interfaces import IRequestPassword, IGSPasswordUser
from .notifier import ResetNotifier


class RequestPasswordResetForm(SiteForm):
    form_fields = form.Fields(IRequestPassword)
    label = 'Reset password'
    pageTemplateFileName = 'browser/templates/request.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        super(RequestPasswordResetForm, self).__init__(context, request)

    @Lazy
    def auditor(self):
        retval = Auditor(self.context, self.siteInfo)
        return retval

    @form.action(label='Reset', failure='handle_set_action_failure')
    def handle_set(self, action, data):
        email = data['email'].strip()
        acl_users = self.context.acl_users
        if address_exists(self.context, email):
            # Send a reset message
            u = acl_users.get_userByEmail(email)
            userInfo = IGSUserInfo(u)
            passwordUser = IGSPasswordUser(u)

            self.auditor.info(REQUEST, userInfo, email)

            # Add the ID to the database
            resetId = self.get_reset_id(userInfo, email)
            # --=mpj17=-- I hope that the verification ID *is* unique
            passwordUser.add_password_reset(resetId)
            # --=mpj17=-- If we get to this point my faith in
            #   non-determinism was warranted.

            #TODO:   think about unverified addresses.
            #        The address that was used is recorded in the audit-table.

            # send the message
            notifier = ResetNotifier(u, self.request)
            resetLink = '{0}/r/password/{1}'.format(self.siteInfo.url, resetId)
            # --=mpj17=-- Note: Unusually for a notification the password-reset
            # notification goes to a *specific* address.
            notifier.notify(self.siteInfo, userInfo, resetLink, email)

            s = 'Instructions on how to reset your password have been sent '\
                'to <code class="email">{0}</code>. Please check your email '\
                '(including the <em>spam</em> or <em>junk</em> folder).'
            self.status = s.format(email)
        else:
            self.auditor.info(REQUEST_FAIL, instanceDatum=email)
            s = 'Your password has <em>not</em> been reset because the '\
                'address <code class="email">{0}</code> is new to us. Please '\
                'enter a different address.'
            self.status = s.format(email)
            self.errors = True

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There was an error:</p>'
        else:
            self.status = '<p>There were errors:</p>'

    def get_reset_id(self, userInfo, email):
        s = email + userInfo.name + self.siteInfo.name + \
            self.siteInfo.get_support_email()
        retval = to_id(s)
        return retval
