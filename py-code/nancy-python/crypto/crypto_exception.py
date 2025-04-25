class CryptoException(Exception):
    """
    crypto base exception. Handled at the outermost level.
    All other exception types are subclasses of this exception type.
    """

class ConfigurationError(CryptoException):
    """
    crypto config exception. Handled at the outermost level.
    All other exception types are subclasses of this exception type.
    """
class DDosProtection(CryptoException):
    """
    crypto DDosProtection exception. Handled at the outermost level.
    """

class RetryableOrderError(CryptoException):
    """
    crypto RetryableOrder exception. Handled at the outermost level.
    """