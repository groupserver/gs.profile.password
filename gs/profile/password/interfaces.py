# coding=utf-8
from zope.interface import Interface

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
        
    def add_password_verification_id(verificationId)
        '''Add a verfication ID to the password-reset table
        
        Arguments
        =========
        
        ``verificationId``
            The verification ID to set.
          
        Side-Effects
        ============
        
        Adds a row to the ``PASSWORD_RESET`` table that contains the
        ``verificationId``.

        Returns
        =======
        
        None.'''
    
    def clear_password_verification_ids():
        '''Clear the password-reset verification IDs for the user.
                
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

