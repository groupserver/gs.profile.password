# coding=utf-8
from zope.component import createObject
from zope.component.factory import Factory
from queries import PasswordUserQuery

class PasswordUser(object):
    def __init__(self, userInfo):
        self.userInfo = userInfo
        self.user = self.context = userInfo.user
        self.__query = None
        
    @property
    def query(self):
        if self.__query == None:
            da = self.context.zsqlalchemy
            self.__query = PasswordUserQuery(da, self.userInfo)
        return self.__query
        
    def set_password(self, password):
        site_root = self.context.site_root()	

        acl_users = site_root.acl_users
        roles = self.user.getRoles()
        domains = self.user.getDomains()
        acl_users.userFolderEditUser(self.userInfo.id, password, roles, 
                                        domains)

        ca = site_root.cookie_authentication
        ca.credentialsChanged(self.user, self.userInfo.id, password)
        
        # TODO: Audit
    
    def add_password_reset(self, resetId):
        raise NotImplementedError('TODO')
    
    def clear_password_reset(self):
        self.query.clear_reset_ids()
        # TODO: Audit

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

