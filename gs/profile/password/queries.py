# coding=utf-8
import pytz, datetime
import sqlalchemy as sa

class PasswordUserQuery(object):
    def __init__(self, da, userInfo=None):
        self.passwordResetTable = da.createTable('password_reset')
        self.userInfo = userInfo
        
    def set_reset_id(self, resetId):
        assert userInfo
        prt = self.passwordResetTable
        i = prt.insert()
        i.execute(verification_id = resetId, 
                    user_id = self.userInfo.id)

    def clear_reset_ids(self):
        assert userInfo
        prt = self.passwordResetTable
        # d = prt.delete(prt.c.user_id == self.user_id)
        u = prt.update(and_(prt.c.user_id == self.userInfo.id,
                            prt.c.reset == None))
        #d.execute()
        d = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        u.execute(reset = d)
        
    def get_userId_from_resetId(self, resetId):
        prt = self.passwordResetTable
        s = prt.select()
        s.append_whereclause(prt.c.verification_id == resetId)

        r = s.execute().fetchone()

        retval = (r and r['user_id']) or ''
        assert type(retval) == str
        return retval
