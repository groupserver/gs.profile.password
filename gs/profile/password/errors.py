# coding=utf-8
from urllib import quote
from zope.component import createObject
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.errormesg.baseerror import BaseErrorPage

class ResetError(BaseErrorPage):
    def __init__(self, context, request):
        BaseErrorPage.__init__(self, context, request)
        self.resetId = request.form.get('resetId', '')
        self.linkAddress = '%s/r/password/%s' % \
            (self.siteInfo.url, self.resetId)      

class ResetIdNotFound(ResetError):
    fileName  = 'browser/templates/reset_id_not_found.pt'
    index = ZopeTwoPageTemplateFile(fileName)
    def __init__(self, context, request):
        ResetError.__init__(self, context, request)
        m = 'Hi! I tried resetting my password using the link %s but '\
            'I saw a Password Reset Error page. I tried... but it '\
            'did not help.' % self.linkAddress
        self.message = quote(m)
        
    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        # Return 404: Not Found
        self.request.response.setStatus(404, lock=True)
        return self.index(self, *args, **kw)

class ResetIdUsed(ResetError):
    fileName  = 'browser/templates/reset_id_used.pt'
    index = ZopeTwoPageTemplateFile(fileName)
    def __init__(self, context, request):
        ResetError.__init__(self, context, request)
        m = 'Hi! I tried resetting my password using the link %s but '\
            'I saw a Password Reset Link Used page. I was trying '\
            'to...' % self.linkAddress
        self.__loggedInUser = None
        self.message = quote(m)

    @property
    def loggedInUser(self):
        if self.__loggedInUser == None:
            self.__loggedInUser = createObject('groupserver.LoggedInUser',
                                    self.context)
        return self.__loggedInUser
        
    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        # Return 410: Gone
        self.request.response.setStatus(410, lock=True)
        return self.index(self, *args, **kw)

class ResetNoId(BaseErrorPage):
    fileName  = 'browser/templates/reset_no_id.pt'
    index = ZopeTwoPageTemplateFile(fileName)
    def __init__(self, context, request):
        BaseErrorPage.__init__(self, context, request)
        self.linkAddress = '%s/r/password/' % self.siteInfo.url
        m = 'Hi! I followed the the link %s but I saw a Password '\
            'Reset Link Error page. I was trying to get to... I found '\
            'the link in...' % self.linkAddress
        self.message = quote(m)
        
    def __call__(self, *args, **kw):
        contentType = 'text/html; charset=UTF-8'
        self.request.response.setHeader('Content-Type', contentType)
        # Return 400: Bad Request
        self.request.response.setStatus(400, lock=True)
        return self.index(self, *args, **kw)

