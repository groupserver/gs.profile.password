Introduction
============

The code for setting, and resetting a password on `GroupServer`_.

Development
===========

The core code for this module was originally written for the
``Products.CustomUserFolder`` module. The code from the old classes was
moved to this new module, and deprication-warnings added to the old code.
 
``CustomUser``
    The code for setting a password, adding a password-reset ID, and
    clearing the password reset IDs was taken from the ``CustomUser``
    and put into the ``PasswordUser``. The latter is set up as an
    adaptor from a user-info to a ``IPasswordUser``.
    
``CustomUserFolder``
    The code for getting a user from a password-reset ID was
    taken from the ``CustomUserFolder`` class and turned into the
    ``groupserver.PasswordUser`` factory. (I know Richard does not like
    them, but a factory is a really useful thing when all you have is
    a string and a context.)
    
``UserQueries``
    The code for performing queries was taken from the old
    ``UserQueries`` class and put into ``PasswordUserQuery``. Some
    quieries hard-coded into the ``CustomUserFolder`` were also moved
    into the new class.

After ensuring I could start my Zope instance,  I started moving code
out of ``Products.GSProfile``. (Yes, the original code was split between
two modules.)

``GSRedirectLogin``
    The code for redirecting the user tackled first. I could test the
    redirector by manually inserting rows into the ``password_reset``
    table. This allowed me to test the ``groupserver.PasswordUser``
    factory, which in turn allowed me to test the queries.

``SetPasswordForm``
    The *Change Password* form has been around for a
    while, and it needed a clean-up. To do this I created the
    ``gs.content.form.form.SiteForm`` abstract base class. The Change
    Password form inherits from that, which cleans up the imports
    a *lot*. 
    
    At this point I also simplified the schema for setting a password. It
    is now a single text entry, rather than two password entries.
    
Changes to SQL
--------------

I altered the ``password_reset`` table on my development platform,
to bring it in line with the code in ``sql/01-password.sql``::
  
  ALTER TABLE password_reset
  ADD COLUMN reset TIMESTAMP WITH TIME ZONE DEFAULT NULL;

.. Resources

.. _GroupServer: http://groupserver.org

