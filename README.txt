=======================
``gs.profile.password``
=======================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Setting passwords for GroupServer site members
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2013-05-16
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 3.0 New Zealand License`_
  by `OnlineGroups.Net`_.

Introduction
============

This product provides the code for setting, and resetting, passwords in
GroupServer_: the pages_ that generate the user interface, the `user
adaptors`_ that actually change the passwords, and the database_
information that controls the password-reset codes. In addition the `show
password toggle`_ JavaScript resource is provided by this product to make
passwords easier to use.

Pages
=====

There are three types of pages currently defined: a `redirector`_, `set
password forms`_ and `error pages`_.

Redirector
----------

The ``gs.profile.password.redirect.RedirectPasswordReset`` code is the core
of the password reset system. It looks up a unique ID in the `database`_
and uses `user adaptors`_ to send a person to the correct reset password
form. While it is not strictly a page it does have many page-like
qualities, including a URL.

Set Password Forms
------------------

There are two forms defined for setting a password.

``gs.profile.password.set.SetPasswordForm``:
  This is the core form for setting a password. I was tempted to say
  "normal" but in all likely hood people will rarely use this page.
  Normally a password is set during sign-up, accepting an invitation, or
  when resetting the password.
  
``gs.profile.password.reset.ResetPasswordForm``:
  Technically a subclass of ``SetPasswordForm``, the *reset* form is shown
  when a person follows a reset-password link. It is a full page form that
  both sets a password and clears the reset-identifiers in the `database`_.

Error Pages
-----------

There are three error pages. All of them are returned by the `redirector`_
in lieu of the reset password form.

``400`` Bad Request:
  This page is shown if no password-reset ID is specified.
  
``404`` Not Found:
  This page is shown if the password-reset ID is not in the
  ``password_reset`` table.

``410`` Gone
  This page is shown if the link has already been followed and a password
  set. Not showing this page is a bug (see `Ticket 326`_)
  
It is typical for sub-systems that log users in — like password
reset, invitations and email-address verification — to have a 400,
404 and 410 errors defined.
  
User Adaptors
=============

There are two user adaptors. One is used by the `redirector`_, the
other is used to alter a password.

The ``IGSPasswordResetUser`` is usually created using a factory
[#factory]_. The `redirector`_ uses the password-reset user to figure out
if the Reset Password page should be shown, or one of the `error pages`_.

The ``IGSPasswordUser`` is used to set a password. It is created by
adapting either a user-instance, or a ``IGSUserInfo`` instance. Its main
job is to set passwords, add entries to the ``password_reset`` table in the
`database`_ or clear entries from the database.

Database
========

The ``password_reset`` table contains all the information required for
resetting a password. The SQL code in ``sql/01-password.sql`` defines three
columns: user ID, password reset ID, and the date that the password was
reset. It is typical for GroupServer code to use dates to signify if a ID
has been used or not. The two classes ``queries.PasswordUserQuery`` and
``queries.PasswordResetQuery`` are used to access the database.

I altered the ``password_reset`` table on my development platform, to bring
it in line with the code in ``sql/01-password.sql``::
  
  ALTER TABLE password_reset
  ADD COLUMN reset TIMESTAMP WITH TIME ZONE DEFAULT NULL;

Show Password Toggle
====================

Passwords are hard to use. They are a (hopefully) long and complex, which
makes it easy to mistype, and hard to recall. In addition the password does
not directly support a user-task: it and obstacle in the way of his or her
task. To make passwords easier to use this product provides a *toggle* on
password-fields to either show the password *en clear* or obscure the
password behind some ``•`` characters [#toggle]_.

The HTML for the toggle is a check-box, formatted like a standard
form-field. The entire widget is given the ``gs-profile-password-toggle``
class::

  <div id="gs-profile-password-set-toggle"
       class="form-widget not-required gs-profile-password-toggle">
    <input id="gs-profile-password-set-toggle-widget" 
           class="checkboxType" type="checkbox" 
           value="1" checked="checked" />
    <label for="gs-profile-password-set-toggle-widget"
           title="Deselect if you are in a public place, like a cafe or library."
                   class="checkboxLabel">Show password</label>
  </div><!--gs-profile-password-set-toggle-->

The ``value`` and ``checked`` fields determine if the password is shown by
default. The convention is:

* *En clear* for setting, and
* Obscured for signing in.

To cause the toggle to toggle the resource
``/++resource++gs-profile-password-toggle-min-20130516.js`` is loaded. It
provides the ``GSProfilePasswordToggle`` class. This takes two arguments:
the selector for the password entry, and the selector for the toggle::

  GSProfilePasswordToggle('#form\\.password1', 
                          '#gs-profile-password-set-toggle-widget');

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.profile.password/
- Questions and comments to http://groupserver.org/groups/development/
- Report bugs at https://redmine.iopen.net/projects/groupserver/

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
.. _Creative Commons Attribution-Share Alike 3.0 New Zealand License:
   http://creativecommons.org/licenses/by-sa/3.0/nz/
.. _Ticket 326: https://projects.iopen.net/groupserver/ticket/326

.. [#factory] I know that Richard does not like factories, but they are
              useful when all you have is a context and an ID.

.. [#toggle] `Ticket 519`_ has more information on why the toggle is
             necessary.

.. _Ticket 519: https://redmine.iopen.net/issues/519
