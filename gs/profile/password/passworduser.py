# coding=utf-8
from zope.component import createObject

class PasswordUser(object):
    def __init__(self, userInfo):
        self.userInfo = userInfo
        self.context = userInfo.user
        
    def set_password(password):
        raise NotImplementedError('TODO')
        
    def add_password_verification(verificationId):
        raise NotImplementedError('TODO')
    
    def clear_password_verification():
        raise NotImplementedError('TODO')

