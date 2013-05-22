# -*- coding: utf-8 -*-
import time
import md5
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore.XWFUtils import convert_int2b62, get_support_email
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.profile.email.base.emailaddress import address_exists
from gs.content.form.form import SiteForm
from gs.profile.notify.interfaces import IGSNotifyUser
from interfaces import IRequestPassword, IGSPasswordUser
from createresetmessage import create_reset_message
from audit import Auditor, REQUEST, REQUEST_FAIL


class RequestPasswordResetForm(SiteForm):
    form_fields = form.Fields(IRequestPassword)
    label = u'Reset Password'
    pageTemplateFileName = 'browser/templates/request.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, context, request):
        super(RequestPasswordResetForm, self).__init__(context, request)

    @Lazy
    def auditor(self):
        retval = Auditor(self.context, self.siteInfo)
        return retval

    @form.action(label=u'Reset', failure='handle_set_action_failure')
    def handle_set(self, action, data):
        email = data['email'].strip()
        acl_users = self.context.acl_users
        if address_exists(self.context, email):
            # Send a reset message
            u = acl_users.get_userByEmail(email)
            userInfo = IGSUserInfo(u)
            notifyUser = IGSNotifyUser(u)
            passwordUser = IGSPasswordUser(u)

            self.auditor.info(REQUEST, userInfo, email)

            # Add the ID to the database
            resetId = self.get_reset_id(userInfo, email)
            # --=mpj17=-- I hope that the verification ID *is* unique
            passwordUser.add_password_reset(resetId)
            # --=mpj17=-- If we get to this point my faith in
            #   non-determinism was warranted.

            #TODO: think about unverified addresses

            # send the message
            fromAddr = get_support_email(self.context, self.siteInfo.id)
            msg = create_reset_message(userInfo, self.siteInfo,
                    email, fromAddr, resetId)
            notifyUser.send_message(msg, email, fromAddr)

            s = u'Instructions on how to reset your password have been sent '\
                u'to <code class="email">{0}</code>. Please check your email '\
                u'(including the <em>spam</em> or <em>junk</em> folder).'
            self.status = s.format(email)
        else:
            self.auditor.info(REQUEST_FAIL, instanceDatum=email)
            s = u'Your password has <em>not</em> been reset because the '\
                u'address <code class="email">{0}</code> is new to us. Please '\
                u'enter a different address.'
            self.status = s.format(email)
            self.errors = True

        assert type(self.status) == unicode

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'There was an error:'
        else:
            self.status = u'<p>There were errors:</p>'

    def get_reset_id(self, userInfo, email):
        s = time.asctime() + email + userInfo.name + self.siteInfo.name
        vNum = long(md5.new(s).hexdigest(), 16)
        resetId = str(convert_int2b62(vNum))
        assert resetId
        return resetId
