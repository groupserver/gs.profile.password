Changelog
=========

3.0.2 (2015-09-21)
------------------

* Fixing the ``maito`` URI, so it uses ``subject=`` rather than
  ``Subject`` (because Google GMail)

3.0.1 (2014-06-11)
------------------

* Using the entered email address, rather than the *preferred*
  address for the *Password reset* notification
* Following the form code to `gs.content.form.base`_ from
  ``gs.content.form``

.. _gs.content.form.base:
   https://github.com/groupserver/gs.content.form.base

3.0.0 (2014-02-28)
------------------

* Switching the *Password reset* email notification to use the
  new HTML email templates
* Ensuring the ``Content-type`` header is set correctly
* Cleaning up some imports
* Switching to Unicode literals

2.0.1 (2013-10-29)
------------------

* Updating the copyright blocks
* Switching to ``absolute_import``

2.0.0 (2013-05-24)
------------------

* Adding the password-visibility toggle to the *Set password*
  page and the *Reset password* page
* Updating to the new GroupServer UI
* Refactoring the JavaScrupt

1.2.3 (2012-08-02)
------------------

* Removing a lock, which is unsupported by ``infrae.wsgi``

1.2.2 (2012-07-03)
------------------

* Fixing a check of the return type

1.2.1 (2012-06-23)
------------------

* Following the update to SQLAlchemy

1.2.0 (2011-06-02)
------------------

* Verifying the email address if there is only one address used
  to reset the password

1.1.2 (2011-01-02)
------------------

* Refactoring for `gs.profile.email.base`_

.. _gs.profile.email.base:
   https://github.com/groupserver/gs.profile.email.base

1.1.1 (2010-12-09)
------------------

* Improving the styling
* Removing unused JavaScript
* Using the new form-message content provider

1.1.0 (2010-11-25)
------------------

* Adding a *Reset password* page
* Adding help
* Adding an auditor
* Adding Python 2.4 compatibility
* Updating the SQL to make it quiet

1.0.0 (2010-11-18)
------------------

Initial version. The core code for this module was originally
written for the ``Products.CustomUserFolder`` module. The code
from the old classes was moved to this new module, and
deprecation-warnings added to the old code.
 
``CustomUser``:
    The code for setting a password, adding a password-reset ID,
    and clearing the password reset IDs was taken from the
    ``CustomUser`` and put into the ``PasswordUser`` user
    adaptor. The new code is simplified, because I cannot think
    of a single case where ``updateCookies`` is not set to true!
    
``CustomUserFolder``:
    The code for getting a user from a password-reset ID was
    taken from the ``CustomUserFolder`` class and turned into the
    ``IGSPasswordResetUser`` factory.
    
``UserQueries``:
    The code for performing queries was taken from the old
    ``UserQueries`` class and put into ``PasswordUserQuery``. The
    queries hard-coded into the ``CustomUserFolder`` were moved
    into the ``PasswordResetQuery``, and jazzed up.

After ensuring I could start my Zope instance, I started moving
code out of ``Products.GSProfile``. (Yes, the original code was
split between two modules.)

``GSRedirectLogin``:
    The code for redirecting the user tackled first. I could test
    the redirector by manually inserting rows into the
    ``password_reset`` table. This allowed me to test the
    ``groupserver.PasswordResetUser`` factory, which in turn
    allowed me to test the `database`_ queries, the `error
    pages`_ and finally the `set password forms`_.

``SetPasswordForm``:
    The ``/r/password`` redirector goes to the *Change Password*
    form.  This was mostly written from scratch, as the old form
    has been around for a while, and it needed a clean-up.  When
    writing this I also simplified the schema for setting a
    password: it is now a single text entry, rather than two
    password entries. I then checked that check that the form
    goes. If I had not finished the code I called ``raise
    NotImplementedError('TODO')``.
