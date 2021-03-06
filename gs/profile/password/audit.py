# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from pytz import UTC
from datetime import datetime
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, AuditQuery, \
    event_id_from_data
from Products.XWFCore.XWFUtils import munge_date

SUBSYSTEM = 'gs.profile.password'
import logging
log = logging.getLogger(SUBSYSTEM)

UNKNOWN = '0'
# password user
SET = '1'
ADD_RESET = '2'  # --=mpj17=-- Not used
CLEAR_RESET = '3'
# request reset
REQUEST = '5'
REQUEST_FAIL = '6'
# redirect
RESET_LOGIN = '7'
RESET_ID_400 = '8'
RESET_ID_404 = '9'
RESET_ID_410 = '10'


class AuditEventFactory(object):
    implements(IFactory)

    title = u'Password Audit-Event Factory'
    description = u'Creates a GroupServer audit event for passwords'

    def __call__(self, context, event_id, code, date, userInfo,
                    instanceUserInfo, siteInfo, groupInfo=None,
                    instanceDatum='', supplementaryDatum='', subsystem=''):
        if code == SET:
            event = SetEvent(context, event_id, date, userInfo, siteInfo)
        elif code == ADD_RESET:
            event = AddResetEvent(context, event_id, date, userInfo,
                        siteInfo)
        elif code == CLEAR_RESET:
            event = ClearResetEvent(context, event_id, date, userInfo,
                        siteInfo)
        elif code == REQUEST:
            event = RequestResetEvent(context, event_id, date, userInfo,
                        siteInfo, instanceDatum)
        elif code == REQUEST_FAIL:
            event = RequestResetFailEvent(context, event_id, date,
                        siteInfo, instanceDatum)
        elif code == RESET_LOGIN:
            event = ResetLoginEvent(context, event_id, date, userInfo,
                        siteInfo)
        elif code == RESET_ID_400:
            event = ResetLoginNoIdEvent(context, event_id, date,
                        siteInfo)
        elif code == RESET_ID_404:
            event = ResetLoginIdNotFoundEvent(context, event_id, date,
                        siteInfo, instanceDatum)
        elif code == RESET_ID_410:
            event = ResetLoginIdUsedEvent(context, event_id, date,
                        userInfo, siteInfo, instanceDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date,
              userInfo, instanceUserInfo, siteInfo, groupInfo,
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


class SetEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person setting a password.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        super(SetEvent, self).__init__(context, id, SET, d, userInfo,
                                userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'%s (%s) set a password on %s (%s).' %\
           (self.userInfo.name, self.userInfo.id,
            self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Set a password.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class AddResetEvent(BasicAuditEvent):
    #--=mpj17=-- Not used, but goes 2010-11-22
    ''' An audit-trail event representing a person resetting a
        password.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        super(AddResetEvent, self).__init__(context, id, ADD_RESET, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'%s (%s) reset a password on %s (%s).' %\
           (self.userInfo.name, self.userInfo.id,
            self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Reset a password.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class ClearResetEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person clearing all reset
        IDs.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        super(ClearResetEvent, self).__init__(context, id, CLEAR_RESET, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'%s (%s) cleared all password reset IDs on %s (%s).' %\
           (self.userInfo.name, self.userInfo.id,
            self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Cleared password reset '\
            u'IDs.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class RequestResetEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person requesting a
        password reset.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo,
                    instanceDatum):
        super(RequestResetEvent, self).__init__(context, id, REQUEST, d,
            userInfo, userInfo, siteInfo, None, instanceDatum, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'%s (%s) requested a password reset on %s (%s). ' \
            u'Used the address <%s>.' %\
            (self.userInfo.name, self.userInfo.id,
            self.siteInfo.name, self.siteInfo.id,
            self.instanceDatum)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Requested password reset '\
            u'using <code class="email">%s</code>.</span>' % \
            (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class RequestResetFailEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person entering in an
    unknown address in the password-reset page.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo, instanceDatum):
        super(RequestResetFailEvent, self).__init__(context, id, REQUEST_FAIL,
            d, None, None, siteInfo, None, instanceDatum, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'Unrecognised address <%s> was used to try and  '\
            u'reset a password reset on %s (%s). ' %\
            (self.instanceDatum,
            self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Unrecognised address '\
            u'<code class="email">%s</code> used to try and reset a'\
            u'password .</span>' % \
            (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class ResetLoginEvent(BasicAuditEvent):
    ''' An audit-trail event representing a person logging in to reset
        his or her password.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, RESET_LOGIN, d,
            userInfo, userInfo, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'Logging in %s (%s) and sending the user to the '\
            u'reset password page on %s (%s). ' %\
            (self.userInfo.name, self.userInfo.id,
             self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Logging in for password '\
            u'reset.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class ResetLoginNoIdEvent(BasicAuditEvent):
    ''' An audit-trail event representing a password-reset with no ID.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo):
        BasicAuditEvent.__init__(self, context, id, RESET_ID_400, d,
            None, None, siteInfo, None, None, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'Password-reset on %s (%s) with no ID.' %\
            (self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">No ID with password '\
            u'reset.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class ResetLoginIdNotFoundEvent(BasicAuditEvent):
    # RESET_ID_404
    ''' An audit-trail event representing a password-reset with no ID.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, RESET_ID_404, d,
            None, None, siteInfo, None, instanceDatum, None, SUBSYSTEM)

    def __unicode__(self):
        retval = u'Password-reset on %s (%s) but the ID was not '\
            u'found (%s).' % \
            (self.siteInfo.name, self.siteInfo.id,
            self.instanceDatum)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Password reset ID %s not '\
            u'found.</span>' % (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class ResetLoginIdUsedEvent(BasicAuditEvent):
    # RESET_ID_410
    ''' An audit-trail event representing someone following a used
    password-reset link.'''
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo,
                instanceDatum):
        BasicAuditEvent.__init__(self, context, id, RESET_ID_410, d,
            userInfo, userInfo, siteInfo, None, instanceDatum, None,
            SUBSYSTEM)

    def __unicode__(self):
        retval = u'The user %s (%s) followed a used password-reset '\
            u'link (%s) on %s (%s).' % \
            (self.userInfo.name, self.userInfo.id,
            self.instanceDatum,
            self.siteInfo.name, self.siteInfo.id)
        return retval

    def __str__(self):
        retval = unicode(self).encode('ascii', 'ignore')
        return retval

    @property
    def xhtml(self):
        cssClass = u'audit-event gs-profile-password-%s' %\
          self.code
        retval = u'<span class="%s">Followed a used password-reset '\
            u'link.</span>' % cssClass
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
        return retval


class Auditor(object):
    def __init__(self, context, siteInfo):
        self.siteInfo = siteInfo
        self.context = context
        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, userInfo='', instanceDatum='', supplementaryDatum=''):
        d = datetime.now(UTC)
        i = userInfo and userInfo or self.siteInfo
        eventId = event_id_from_data(i, i, self.siteInfo, code,
                    instanceDatum, supplementaryDatum)

        e = self.factory(self.context, eventId, code, d, userInfo, userInfo,
                self.siteInfo, None, instanceDatum, supplementaryDatum,
                SUBSYSTEM)

        self.queries.store(e)
        log.info(e)
