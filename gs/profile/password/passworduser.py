# coding=utf-8
from zope.component import createObject
from zope.component.factory import Factory
from queries import PasswordUserQuery

class PasswordUser(object):
    def __init__(self, userInfo):
        self.userInfo = userInfo
        self.context = userInfo.user
        
    def set_password(self, password):
        # TODO: Audit
        raise NotImplementedError('TODO')
        
    def add_password_reset(self, resetId):
        raise NotImplementedError('TODO')
    
    def clear_password_reset(self):
        raise NotImplementedError('TODO')

class PasswordUserFromId(object):
    '''Create a Password User from a Reset ID
    
    We do not always have a IGSUserInfo to hand when we want a password
    user. Sometimes we have a password-reset ID.'''
    def __call__(self, context, resetId):
    
        da = context.zsqlalchemy
        queries = PasswordUserQuery(da)
        
        uid = queries.get_userId_from_resetId(resetId)
        assert uid, 'Cound not get a user ID for the reset ID %s' % resetID
        
        userInfo = createObject('groupserver.UserFromId', context, uid)
        return PasswordUser(userInfo)

PasswordUserFactory = Factory(
                        PasswordUserFromId, 
                        'Password User from ID',
                        'Create a password user from a reset ID.')

