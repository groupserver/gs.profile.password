# coding=utf-8
import pytz, datetime
import sqlalchemy as sa
from gs.database import getTable, getSession
from zope.sqlalchemy import mark_changed

class PasswordUserQuery(object):
    def __init__(self, userInfo):
        self.passwordResetTable = getTable('password_reset')
        assert userInfo
        self.userInfo = userInfo
        
    def set_reset_id(self, resetId):
        prt = self.passwordResetTable
        i = prt.insert()
        session = getSession()
        session.execute(i, params={'verification_id': resetId, 
                                   'user_id': self.userInfo.id})
        mark_changed(session)

    def clear_reset_ids(self):
        prt = self.passwordResetTable
        u = prt.update(sa.and_(prt.c.user_id == self.userInfo.id,
                                prt.c.reset == None))
        d = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        session = getSession()
        session.execute(u, params={'reset': d})
        mark_changed(session)

class PasswordResetQuery(object):
    NOT_FOUND  = 0
    CURRENT   = 1
    RESET     = 2
    def __init__(self):
        self.passwordResetTable = getTable('password_reset')
        
    def get_userId_from_resetId(self, resetId):
        prt = self.passwordResetTable
        s = prt.select()
        s.append_whereclause(prt.c.verification_id == resetId)

        session = getSession()
        r = session.execute(s).fetchone()

        retval = (r and r['user_id']) or ''
        assert type(retval) in (str, unicode), \
            'Wrong return type %s' % type(retval)
        return retval

    def resetId_status(self, resetId):
        prt = self.passwordResetTable
        s = prt.select()
        s.append_whereclause(prt.c.verification_id == resetId)
        
        session = getSession()
        r  = session.execute(s).fetchone()
        
        if r:
            if r['reset'] == None:
                retval = self.CURRENT
            else:
                retval = self.RESET
        else:
            retval = self.NOT_FOUND
        assert retval in (self.NOT_FOUND, self.CURRENT, self.RESET)
        return retval

