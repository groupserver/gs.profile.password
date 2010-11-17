# coding=utf-8
import pytz, datetime
import sqlalchemy as sa

class PasswordUserQuery(object):
    def __init__(self, da, userInfo):
        self.passwordResetTable = da.createTable('password_reset')
        self.userInfo = userInfo
        
    def set_reset_id(self, resetId):
        assert userInfo
        prt = self.passwordResetTable
        i = prt.insert()
        i.execute(verification_id = resetId, 
                    user_id = self.userInfo.id)

    def clear_reset_ids(self):
        assert self.userInfo
        prt = self.passwordResetTable
        u = prt.update(sa.and_(prt.c.user_id == self.userInfo.id,
                                prt.c.reset == None))
        d = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        u.execute(reset = d)

class PasswordResetQuery(object):
    NOT_FOUND  = 0
    CURRENT   = 1
    RESET     = 2
    def __init__(self, da):
        self.passwordResetTable = da.createTable('password_reset')
        
    def get_userId_from_resetId(self, resetId):
        # TODO: Move to a different class, which the IGSResetPasswordUser
        # factory can use.
        prt = self.passwordResetTable
        s = prt.select()
        s.append_whereclause(prt.c.verification_id == resetId)

        r = s.execute().fetchone()

        retval = (r and r['user_id']) or ''
        assert type(retval) == str
        return retval

    def resetId_status(self, resetId):
        prt = self.passwordResetTable
        s = prt.select()
        s.append_whereclause(prt.c.verification_id == resetId)
        
        r  = s.execute().fetchone()
        
        if r:
            if r['reset'] == None:
                retval = self.CURRENT
            else:
                retval = self.RESET
        else:
            retval = self.NOT_FOUND
        assert retval in (self.NOT_FOUND, self.CURRENT, self.RESET)
        return retval

