"""
Custom exceptions for Drivault application.
These exceptions are used to handle domain-specific errors.
"""

class DrivaultException(Exception):
    """Base exception for all Drivault custom exceptions"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UserAlreadyExistsException(DrivaultException):
    """Raised when attempting to create a user that already exists"""
    def __init__(self, message: str = "User already exists with this email"):
        super().__init__(message, status_code=400)


class UserNotFoundException(DrivaultException):
    """Raised when a user is not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, status_code=404)


class InvalidCredentialsException(DrivaultException):
    """Raised when login credentials are invalid"""
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message, status_code=401)


class FileNotFoundException(DrivaultException):
    """Raised when a file is not found"""
    def __init__(self, message: str = "File not found"):
        super().__init__(message, status_code=404)


class StorageConfigurationException(DrivaultException):
    """Raised when storage path configuration is invalid"""
    def __init__(self, message: str = "Invalid storage configuration"):
        super().__init__(message, status_code=500)