# coding=utf-8
from zope.component import createObject
from Products.GSRedirect.view import GSRedirectBase
from Products.GSProfile.utils import login
from resetuser import ResetIdNotFoundError
from audit import Auditor, RESET_LOGIN, RESET_ID_400

class RedirectPasswordReset(GSRedirectBase):
    def __call__(self):
        siteInfo = createObject('groupserver.SiteInfo', self.context)
        auditor = Auditor(self.context, siteInfo)
        
        if len(self.traverse_subpath) == 1:
            # The reset ID is specified
            resetId = self.traverse_subpath[0]
            try:
                passwordResetUser = \
                    createObject('groupserver.PasswordResetUser', 
                                    self.context, resetId)
            except ResetIdNotFoundError as e:
                # TODO: audit
                uri = '/password-reset-not-found.html?resetId=%s' % \
                    resetId
            else:
                if passwordResetUser.resetId_current(resetId):
                    auditor.info(RESET_LOGIN, passwordResetUser)
                    # Only log in when resetting the password
                    login(self.context, passwordResetUser.user)
                    uri = passwordResetUser.passwordSetUrl
                else:
                    # TODO: audit
                    uri = '/password-reset-used.html?resetId=%s' %\
                        resetId                
        else:
            auditor.info(RESET_ID_400)
            # the reset ID is not specified
            uri = '/password-reset-no-id.html'
        assert uri, 'URI not set'
        return self.request.RESPONSE.redirect(uri)

