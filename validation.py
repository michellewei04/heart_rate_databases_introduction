from jsonschema import validate, ValidationError, FormatChecker
import datetime


email_format = {
    "type": "string",
    "format": "email"
}


heart_rate_input_type = {
    "type": "object",
    "properties": {
        "user_email": {
            "type": "string",
            "format": "email"
        },
        "user_age": {
            "type": "integer",
            "minimum": 0
        },
        "heart_rate": {
            "type": "integer",
            "minimum": 0
        }
    },
    'required': ['user_email', 'user_age', 'heart_rate']
}

interval_average_input_type = {
    "type": "object",
    "properties": {
        "user_email": {
            "type": "string",
            "format": "email"
        },
        "heart_rate_average_since": "string"
    }
}


def validate_email_format(email):
    try:
        validate(email, email_format, format_checker=FormatChecker())
        return True
    except ValidationError:
        return False


def validate_hr_input(hr):
    try:
        validate(hr, heart_rate_input_type, format_checker=FormatChecker())
        return True
    except ValidationError:
        return False


def validate_date_time_input(date_time):
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    try:
        datetime.datetime.strptime(date_time, time_format)
        return True
    except ValueError:
        return ValueError
    except TypeError:
        return TypeError
