# coding=utf-8
from zope.component import createObject
from zope.component.factory import Factory
from queries import PasswordResetQuery
from Products.CustomUserFolder.userinfo import GSUserInfo

class ResetPasswordUser(GSUserInfo):
    def __init__(self, userInfo):
        GSUserInfo.__init__(self, userInfo.user)
        self.__passwordSetUrl = self.__query = None
        
    @property
    def passwordSetUrl(self):
        if self.__passwordSetUrl == None:
            self.__passwordSetUrl = '%s/reset_password.html' % self.url
        return self.__passwordSetUrl
    
    @property
    def query(self):
        if self.__query == None:
            da = self.user.zsqlalchemy
            self.__query = PasswordResetQuery(da)
        return self.__query
        
    def resetId_current(self, resetId):
        return self.query.resetId_status(resetId) == self.query.CURRENT
    
    def resetId_exists(self, resetId):
        return self.query.resetId_status(resetId) != self.query.NOT_FOUND

class ResetIdNotFoundError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return 'Counld not find reset ID (%s)' % self.value

class ResetPasswordUserFromId(object):
    '''Create a Password User from a Reset ID
    
    We do not always have a IGSUserInfo to hand when we want a password
    user. Sometimes we have a password-reset ID.'''
    def __call__(self, context, resetId):
    
        da = context.zsqlalchemy
        queries = PasswordResetQuery(da)
        
        s = queries.resetId_status(resetId)
        if s == queries.NOT_FOUND:
            raise ResetIdNotFoundError(resetId)

        uid = queries.get_userId_from_resetId(resetId)
        userInfo = createObject('groupserver.UserFromId', context, uid)
        return ResetPasswordUser(userInfo)

ResetPasswordUserFactory = Factory(
                        ResetPasswordUserFromId, 
                        'Reset-Password User from ID',
                        'Create a reset-password user from a reset ID.')

