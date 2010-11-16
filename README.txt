Introduction
============

The code for setting, and resetting a password on `GroupServer`_.

Development
===========

The core code for this module was originally written for the ``Products.CustomUserFolder`` module. 

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

After ensuring I could start my Zope instance,  I started moving the
code out of ``Products.GSProfile``. (Yes, the original code was messy.)

``GSRedirectLogin``
    The code for redirecting the user tackled first.

.. Resources

.. _GroupServer: http://groupserver.org

