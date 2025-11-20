from pydantic import ValidationError


class ModelErrorException(Exception):
    """
    Custom exception for model errors, including property name and error message.
    """

    def __init__(self, error: ValidationError):

        errors = error.errors()
        if errors:
            property_name = errors[0].get('loc', ['unknown'])[0]
            developer_message = errors[0].get('msg', 'Validation error')
        else:
            property_name = 'unknown'
            developer_message = 'Validation error'

        self.property_name = property_name
        self.user_message = "Invalid data provided."
        self.developer_message = developer_message
        super().__init__(self.user_message)

    def primitives(self) -> dict:
        return {
            "property": self.property_name,
            "user_message": self.user_message,
            "developer_message": self.developer_message
        }

    @staticmethod
    def generate_primitives(error: ValidationError) -> dict:
        instance = ModelErrorException(error)
        return instance.primitives()
