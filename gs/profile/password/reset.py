# coding=utf-8
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from set import SetPasswordForm
from interfaces import IGSPasswordUser

class ResetPasswordForm(SetPasswordForm):
    label = u'Change Password'
    pageTemplateFileName = 'browser/templates/reset.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    @form.action(label=u'Change', failure='handle_set_action_failure')
    def handle_set(self, action, data):
       
        # Using the logged in user, rather than self.context is
        # deliberate. By using the logged in user we prevent anyone from
        # even *accidently* changing the password of another user.
        liu = createObject('groupserver.LoggedInUser', self.context)
        assert not(liu.anonymous), 'Not logged in'
        pu = IGSPasswordUser(liu)
        pu.set_password(data['password1'])
        pu.clear_password_reset()
                
        self.status = u'Your password has been changed. ' \
          'You can now '\
          '<strong>go to <a href="%s">your profile</a></strong> '\
          'to view your groups.' % self.userInfo.url
        assert type(self.status) == unicode

