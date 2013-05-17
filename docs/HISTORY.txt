Changelog
=========

Development History
===================

The core code for this module was originally written for the
``Products.CustomUserFolder`` module. The code from the old classes was
moved to this new module, and deprecation-warnings added to the old code.
 
``CustomUser``:
    The code for setting a password, adding a password-reset ID, and
    clearing the password reset IDs was taken from the ``CustomUser`` and
    put into the ``PasswordUser`` user adaptor. The new code is simplified,
    because I cannot think of a single case where ``updateCookies`` is not
    set to true!
    
``CustomUserFolder``:
    The code for getting a user from a password-reset ID was taken from the
    ``CustomUserFolder`` class and turned into the ``IGSPasswordResetUser``
    factory.
    
``UserQueries``:
    The code for performing queries was taken from the old ``UserQueries``
    class and put into ``PasswordUserQuery``. The queries hard-coded into
    the ``CustomUserFolder`` were moved into the ``PasswordResetQuery``,
    and jazzed up.

After ensuring I could start my Zope instance, I started moving code out of
``Products.GSProfile``. (Yes, the original code was split between two
modules.)

``GSRedirectLogin``:
    The code for redirecting the user tackled first. I could test the
    redirector by manually inserting rows into the ``password_reset``
    table. This allowed me to test the ``groupserver.PasswordResetUser``
    factory, which in turn allowed me to test the `database`_ queries, the
    `error pages`_ and finally the `set password forms`_.

``SetPasswordForm``:
    The ``/r/password`` redirector goes to the *Change Password* form.
    This was mostly written from scratch, as the old form has been around
    for a while, and it needed a clean-up.  When writing this I also
    simplified the schema for setting a password: it is now a single text
    entry, rather than two password entries. I then checked that check that
    the form goes. If I had not finished the code I called ``raise
    NotImplementedError('TODO')``.
