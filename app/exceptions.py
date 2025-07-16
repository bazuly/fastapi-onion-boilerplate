from uuid import UUID

from fastapi import HTTPException, status


class BaseAppError(Exception):
    """Base exception for all application errors."""

    pass


class ApplicationNotFound(BaseAppError):
    """Exception raised when an application cannot be found."""

    def __init__(self, user_name: str):
        self.user_name = user_name
        message = (
            f"Application for '{user_name}' not found."
            if user_name
            else "No available applications."
        )
        super().__init__(message)


class ImageUploadError(Exception):
    """Base exception for all image upload errors."""

    pass


class ImageNotFoundError(ImageUploadError):
    """Exception raised when an image cannot be found."""

    def __init__(self, image_id: int | UUID):
        self.image_id = image_id
        super().__init__(f"Image not found. ID: {image_id}")


class DatabaseError(Exception):
    """Base exception for all database errors."""

    pass


class DatabaseConnectionError(DatabaseError):
    """Exception raised when a database connection cannot be established."""

    def __init__(self, details: str):
        self.details = details
        message = "Failed to connect to database."
        if details:
            message += f" Details: {details}"
        super().__init__(message)


class RepositoryError(DatabaseError):
    """Default repository exception."""

    def __init__(self, message: str = "Repository error"):
        super().__init__(message)


class KafkaError(Exception):
    """Base exception for Kafka consumer/producer errors."""

    default_message = "Kafka error occurred."

    def __init__(self, details: str):
        self.details = details
        message = self.default_message
        if details:
            message += f" Details: {details}"
        super().__init__(message)


class ConsumerError(KafkaError):
    default_message = "Failed to consume message, break."


class ProducerError(KafkaError):
    default_message = "Failed to produce message, reload..."


class KafkaMessageError(KafkaError):
    default_message = "Failed to send message, break..."


class KafkaImageDataUploadError(KafkaError):
    default_message = "Failed to send image data"


class CrudException(HTTPException):
    def __init__(
            self,
            detail: str = "CRUD operation error",
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(status_code=status_code, detail=detail)


class UserLogException(HTTPException):
    def __init__(self, operation: str):
        detail = f"Audit failed for operation: {operation}"
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MongoException(Exception):
    """Base exception for Mongo errors."""

    default_message = "Mongo error occurred."

    def __init__(self, details: str):
        self.details = details
        message = self.default_message
        if details:
            message += f" Details: {details}"
        super().__init__(message)


class RecordMongoException(MongoException):
    default_message = "Failed to record data into mongo DB"
