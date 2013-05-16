# -*- coding: utf-8 -*-
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from zope.component.factory import Factory
from queries import PasswordResetQuery
from Products.CustomUserFolder.userinfo import GSUserInfo


class ResetPasswordUser(GSUserInfo):
    def __init__(self, userInfo):
        super(ResetPasswordUser, self).__init__(userInfo.user)

    @Lazy
    def passwordSetUrl(self):
        retval = '{0}/reset_password.html'.format(self.url)
        return retval

    @Lazy
    def query(self):
        retval = PasswordResetQuery()
        return retval

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
        queries = PasswordResetQuery()

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
