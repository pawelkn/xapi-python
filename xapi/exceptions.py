class LoginFailed(Exception):
    """
    Raised when a log in failed.
    """

class ConnectionClosed(Exception):
    """
    Raised when a connection was never opened or closed unexpectedly.
    """