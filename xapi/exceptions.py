class LoginFailed(Exception):
    """
    Raised when a log in failed.
    """

class ConnectionClosed(Exception):
    """
    Raised when a connection has never been opened or closed unexpectedly.
    """