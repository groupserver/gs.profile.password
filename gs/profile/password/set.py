# coding=utf-8
from zope.component import createObject
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.XWFCore import XWFUtils
from Products.CustomUserFolder.interfaces import IGSUserInfo
from gs.content.form.form import SiteForm
from interfaces import ISetPassword, IGSPasswordUser

class SetPasswordForm(SiteForm):
    form_fields = form.Fields(ISetPassword)
    label = u'Change Password'
    pageTemplateFileName = 'browser/templates/set.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)

    def __init__(self, user, request):
        SiteForm.__init__(self, user, request)
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
        pu.clear_password_reset()
                
        self.status = u'Your password has been changed.'
        assert type(self.status) == unicode

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = u'There was an error:'
        else:
            self.status = u'<p>There were errors:</p>'

