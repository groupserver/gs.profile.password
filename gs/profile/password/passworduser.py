# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from queries import PasswordUserQuery
from audit import Auditor, SET, CLEAR_RESET


class PasswordUser(object):
    def __init__(self, userInfo):
        self.userInfo = userInfo
        self.user = self.context = userInfo.user

    @Lazy
    def auditor(self):
        si = createObject('groupserver.SiteInfo', self.context)
        retval = Auditor(self.context, si)
        return retval

    @Lazy
    def query(self):
        retval = PasswordUserQuery(self.userInfo)
        return retval

    def set_password(self, password):
        site_root = self.context.site_root()

        acl_users = site_root.acl_users
        roles = self.user.getRoles()
        domains = self.user.getDomains()
        acl_users.userFolderEditUser(self.userInfo.id, password, roles, domains)

        ca = site_root.cookie_authentication
        ca.credentialsChanged(self.user, self.userInfo.id, password)

        self.auditor.info(SET, self.userInfo)

    def add_password_reset(self, resetId):
        self.query.set_reset_id(resetId)
        # --=mpj17=-- Don't bother. This will not add munch information
        # self.auditor.info(ADD_RESET, self.userInfo)

    def clear_password_reset(self):
        self.query.clear_reset_ids()
        self.auditor.info(CLEAR_RESET, self.userInfo)
