class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {"message": "Something went wrong", "status": 500},
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400,
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400,
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401,
    },
}
