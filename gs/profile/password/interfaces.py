# coding=utf-8
from zope.interface import Interface
from zope.schema import ASCIILine
from Products.CustomUserFolder.interfaces import IGSUserInfo

class IGSPasswordUser(Interface):
    '''A user who can manipulate passwords'''

    def set_password(password):
        '''Set the password for a user.
       
       Arguments
       =========
       
       ``password``
           The new password.

        SIDE-EFFECTS
        ============
        
        Changes the passwored stored in ``site_root.acl_users`` and the
        cookie (authentication information) stored in 
        ``site_root.cookie_authentication``.

        RETURNS
        =======
        
        None.'''
        
    def add_password_reset_id(resetId):
        '''Add a verfication ID to the password-reset table
        
        Arguments
        =========
        
        ``resetId``
            The reset ID to set.
          
        Side-Effects
        ============
        
        Adds a row to the ``PASSWORD_RESET`` table that contains the
        ``resetId``.

        Returns
        =======
        
        None.'''
    
    def clear_password_reset():
        '''Clear the password-reset reset IDs for the user.
                
        Arguments
        =========

        None.
          
        Side-Effects
        ============
        
        Every row in the ``PASSWORD_RESET`` table that has not been
        used is marked as used.

        Returns
        =======
        
        None.'''


class IGSPasswordResetUser(IGSUserInfo):
    def resetId_exists(resetId):
        '''Is the reset ID exists
        
        Arguments
        =========
        
        The reset ID.
        
        Side-Effects
        ============
        
        None.
        
        Returns
        =======
        
        ``True`` if the reset ID is exists, regardless of whether it is 
        current or not; ``False`` otherwise.'''

    def resetId_current(resetId):
        '''Is the reset ID current
        
        Arguments
        =========
        
        The reset ID.
        
        Side-Effects
        ============
        
        None.
        
        Returns
        =======
        
        ``True`` if the reset ID is current; ``False`` otherwise.'''

    passwordSetUrl = ASCIILine(title=u'URL for the Set Password page',
        description=u'The URL for the Set Password page for the user.',
        required=True)

class ISetPassword(Interface):
    """Schema for setting the user's password."""
      
    password1 = ASCIILine(title=u'Password',
        description=u'Your new password. For security, your password '\
          u'should contain a mixture of letters and numbers, and '\
          u'must be over four letters long.',
        required=True,
        min_length=4)

