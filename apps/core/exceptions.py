from rest_framework import status
from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    """Base exception for all API errors with consistent structure."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"
    default_detail = "An error occurred."

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        super().__init__(detail={"detail": detail, "code": code})


class AlreadyRegisteredError(BaseAPIException):
    """Raised when user tries to register for an event they're already registered for."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "already_registered"
    default_detail = "You are already registered for this event."


class NotRegisteredError(BaseAPIException):
    """Raised when user tries to unregister from an event they're not registered for."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "not_registered"
    default_detail = "You are not registered for this event."


class PasswordMismatchError(BaseAPIException):
    """Raised when password confirmation doesn't match."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "password_mismatch"
    default_detail = "Passwords don't match."


class EmailAlreadyExistsError(BaseAPIException):
    """Raised when email is already taken."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "email_exists"
    default_detail = "User with this email already exists."


class UsernameAlreadyExistsError(BaseAPIException):
    """Raised when username is already taken."""

    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "username_exists"
    default_detail = "User with this username already exists."


class EventNotFoundError(BaseAPIException):
    """Raised when event is not found."""

    status_code = status.HTTP_404_NOT_FOUND
    default_code = "event_not_found"
    default_detail = "Event not found."


class PermissionDeniedError(BaseAPIException):
    """Raised when user doesn't have permission for an action."""

    status_code = status.HTTP_403_FORBIDDEN
    default_code = "permission_denied"
    default_detail = "You don't have permission to perform this action."
