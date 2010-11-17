Introduction
============

The profile-password code is divided into three main parts: `pages`_, `user adaptors`_ and `database`_.

Pages
=====

There are three types of pages currently defined: a `redirector`_,
`set password forms`_ and `error pages`_.

Redirector
----------

The ``gs.profile.password.redirect.RedirectPasswordReset`` code is
the core of the password reset system. It looks up a unique ID in the
`database`_ and uses `user adaptors`_ to send a person to the correct
reset password form. While it is not strictly a page it does have many
page-like qualities, including a URL.

Set Password Forms
------------------

There are two forms defined for setting a password.

``gs.profile.password.set.SetPasswordForm``
  This is the core form for setting a password. I was tempted to say 
  "normal" but in all likely hood people will rarely use this page.
  Normally a password is set during sign-up, accepting an invitation,
  or when resetting the password.
  
``gs.profile.password.reset.ResetPasswordForm``
  Technically a subclass of ``SetPasswordForm``, the *reset* form is
  shown when a person follows a reset-password link. It is a full page
  form that both sets a password and clears the reset-identifiers in 
  the `database`_.

Error Pages
-----------

There are three error pages. All of them are returned by the
`redirector`_ in lieu of the reset password form.

400 Bad Request
  This page is shown if no password-reset ID is specified.
  
404 Not Found
  This page is shown if the password-reset ID is not in the
  ``password_reset`` table.

410 Gone
  This page is shown if the link has already been followed and a
  password set. Not showing this page is a bug (see `Ticket 326`_) 

  
It is typical for sub-systems that log users in — like password
reset, invitations and email-address verification — to have a 400,
404 and 410 errors defined.
  
User Adaptors
=============

There are two user adaptors. One is used by the `redirector`_, the
other is used to alter a password.

The ``IGSPasswordResetUser`` is usually created using a factory. (I know
that Richard does not like factories, but they are useful when all you
have is a context and an ID.) The `redirector`_ uses the password-reset
user to figure out if the Reset Password page should be shown, or one
of the `error pages`_.

The ``IGSPasswordUser`` is used to set a password. It is created by
adapting either a user-instance, or a ``IGSUserInfo`` instance. Its
main job is to set passwords, add entries to the ``password_reset``
table in the `database`_ or clear entries from the database.

Database
========

The ``password_reset`` table contains all the information required for
resetting a password. The SQL code in ``sql/01-password.sql`` defines
three columns: user ID, password reset ID, and the date that the password
was reset. It is typical for GroupServer code to use dates to signify if
a ID has been used or not. The two classes ``queries.PasswordUserQuery``
and ``queries.PasswordResetQuery`` are used to access the database.

I altered the ``password_reset`` table on my development platform,
to bring it in line with the code in ``sql/01-password.sql``::
  
  ALTER TABLE password_reset
  ADD COLUMN reset TIMESTAMP WITH TIME ZONE DEFAULT NULL;


Development
===========

The core code for this module was originally written for the
``Products.CustomUserFolder`` module. The code from the old classes was
moved to this new module, and deprecation-warnings added to the old code.
 
``CustomUser``
    The code for setting a password, adding a password-reset ID, and
    clearing the password reset IDs was taken from the ``CustomUser``
    and put into the ``PasswordUser`` user adaptor. The new code is 
    simplified, because I cannot think of a single case where
    ``updateCookies`` is not set to true! 
    
``CustomUserFolder``
    The code for getting a user from a password-reset ID was
    taken from the ``CustomUserFolder`` class and turned into the
    ``IGSPasswordResetUser`` factory. 
    
``UserQueries``
    The code for performing queries was taken from the old
    ``UserQueries`` class and put into ``PasswordUserQuery``. The
    queries hard-coded into the ``CustomUserFolder`` were moved into the
    ``PasswordResetQuery``, and jazzed up.

After ensuring I could start my Zope instance,  I started moving code
out of ``Products.GSProfile``. (Yes, the original code was split between
two modules.)

``GSRedirectLogin``
    The code for redirecting the user tackled first. I could test the
    redirector by manually inserting rows into the ``password_reset``
    table. This allowed me to test the ``groupserver.PasswordResetUser``
    factory, which in turn allowed me to test the `database`_ queries,
    the `error pages`_ and finally the `set password forms`_.

``SetPasswordForm``
    The ``/r/password`` redirector goes to the *Change Password* form.
    This was mostly written from scratch, as the old form has been around
    for a while, and it needed a clean-up.  When writing this I also
    simplified the schema for setting a password: it is now a single
    text entry, rather than two password entries. I then checked that
    check that the form goes. If I had not finished the code I called
    ``raise NotImplementedError('TODO')``.

.. Resources

.. _GroupServer: http://groupserver.org
.. _Ticket 326: https://projects.iopen.net/groupserver/ticket/326

