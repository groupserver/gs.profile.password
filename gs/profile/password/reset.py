# coding=utf-8
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.profile.email.base.emailuser import EmailUser
from gs.profile.email.verify.emailverificationuser import EmailVerificationUser
from set import SetPasswordForm
from interfaces import IGSPasswordUser

class ResetPasswordForm(SetPasswordForm):
    label = u'Change Password'
    pageTemplateFileName = 'browser/templates/reset.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    @Lazy
    def loggedInUser(self):
        retval = createObject('groupserver.LoggedInUser', self.context)
        assert not(retval.anonymous), 'Not logged in'
        return retval
        
    @form.action(label=u'Change', failure='handle_set_action_failure')
    def handle_set(self, action, data):
        self.set_password(data['password1'])
        self.verify_email()

        self.status = u'Your password has been changed. ' \
          'You can now '\
          '<strong>go to <a href="%s">your profile</a></strong> '\
          'to view your groups.' % self.userInfo.url
        assert type(self.status) == unicode

    def set_password(self, password):
        # Using the logged in user, rather than self.context is
        # deliberate. By using the logged in user we prevent anyone from
        # even *accidently* changing the password of another user.
        pu = IGSPasswordUser(self.loggedInUser)
        pu.set_password(password)
        pu.clear_password_reset()

    def verify_email(self):
        # Ticket 480: Password Reset Should Verify Email Address
        # <https://projects.iopen.net/groupserver/ticket/480>
        # If A user only has one email address (most people),
        #   and that address is unverified,
        eu = EmailUser(self.context, self.loggedInUser)
        if ((len(eu.get_addresses()) == 1) 
            and (len(eu.get_unverified_addresses()) == 1)):
            #  then the email address should be verified.
            email = eu.get_addresses()[0]
            evu = EmailVerificationUser(self.context, self.loggedInUser, 
                                        email)
            vid = '%s-password' % evu.create_verification_id()
            evu.add_verification_id(vid)
            evu.verify_email(vid)

