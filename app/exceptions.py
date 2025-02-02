class ApplicationNotFound(Exception):

    @staticmethod
    def detail(user_name):
        return f"Application for '{user_name}' not found."

    @staticmethod
    def no_available_applications(self):
        return print("No available applications.")
