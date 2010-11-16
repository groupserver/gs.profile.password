# coding=utf-8
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from interfaces import *
from Products.GSProfile.utils import login

class RedirectPasswordReset(GSRedirectBase):
    def __call__(self):
        site_root = self.context.site_root()
        acl_users = site_root.acl_users

        if len(self.traverse_subpath) == 1:
            resetId = self.traverse_subpath[0]
            pu = createObject('groupserver.PasswordUser', context, resetId)
                        
            if pu:
                userInfo = pu.userInfo
                # TODO: audit
                login(self.context, userInfo.user)
                
                uri = '%s/password.html' % userInfo.url
            else: # Cannot find user
                uri = '/user-not-found?id=%s' % verificationId
        else: # Verification ID not specified
            uri = '/user-no-id'
        return self.request.RESPONSE.redirect(uri)

