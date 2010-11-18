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
        self.query.set_reset_id(resetId)
        # TODO: Audit
    
    def clear_password_reset(self):
        self.query.clear_reset_ids()
        # TODO: Audit

