"""
plasmapy.utils.exceptions
===============

Custom Error and Warning names to improve readability
"""


# ----------
# Exceptions:
# ----------

class PlasmaPyError(Exception):
    """Base class of any error raised by PlasmaPy.
    
    All exceptions raised by PlasmaPy should inherit from this class, including
    custom exceptions defined in this module.
    
    Custom exceptions can inherit from other exception types too. Thus, if code
    already knows how to handle a ValueError, it won't need any specific
    modification.
    """

class PhysicsError(PlasmaPyError, ValueError):
    """Error for use of a physics value outside PlasmaPy theoretical bounds"""

class RelativityError(PhysicsError):
    """Error for use of a speed greater than or equal to the speed of light"""



# ----------
# Warnings:
# ----------    

class PlasmaPyWarning(Warning):
    """Base class of any warning issued by PlasmaPy
    
    All warnings issued by PlasmaPy should inherit from this class, including
    custom warnings defined in this module.
    
    Warnings should be issued using warnings.warn, which will not break
    execution if unhandled. 
    """

class PhysicsWarning(PlasmaPyWarning):
    """Warning for using a mildly worrisome physics value"""

class RelativityWarning(PhysicsWarning):
    """Warning for use of a speed quantity approaching the speed of light"""

