# -*- coding: utf-8 -*-
from Products.GSAuditTrail.queries import AuditQuery
from audit import SET, SUBSYSTEM


def password_set(context, user):
    '''Check if a password has ever been set.

Description
-----------

We cannot check the password itself to see if the password is blank,
because it may be hashed in all sorts of ways, so a blank password
does no look blank. Instead this little method looks in the audit-trail
for a profile-event that corresponds to a member setting a password.

Arguments
---------

  * ``context``: The Zope context, which is used to find the data
    adapter.
  * ``user``: The GroupServer CustomUser instance that is to be checked.

Returns
-------

Boolean, True if a password has been set.

Side Effects
------------

None.

Acknowledgements
---------------

Thanks to Alice for suggesting that I trawl the audit-logs for the
set-password events.'''
    q = AuditQuery()
    items = q.get_instance_user_events(user.getId(), limit=128)
    setPasswordItems = [i for i in items if ((i['subsystem'] == SUBSYSTEM) and
                                                 (i['code'] == SET))]
    retval = bool(setPasswordItems)
    return retval
