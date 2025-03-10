from uuid import UUID


class ApplicationNotFound(Exception):

    @staticmethod
    def detail(user_name):
        raise f"Application for '{user_name}' not found."

    @staticmethod
    def no_available_applications(self):
        raise "No available applications."


class ImageUploadRepositoryException(Exception):
    @staticmethod
    def database_query_error():
        raise f"Database/repository error, probably filename already exists."

    @staticmethod
    def image_not_found_error(image_id: int | UUID):
        raise f"Image not found. {image_id}"
