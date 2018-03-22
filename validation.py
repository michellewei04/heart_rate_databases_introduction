from jsonschema import validate, ValidationError
import datetime

hr_type = {
    "type": "object",
    "properties": {
        "user_email": "string",
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

time_since_type = {
    "type": "object",
    "properties": {
        "user_email": "string",
        "heart_rate_average_since": "string"
    }
}


def validate_hr(hr):
    try:
        validate(hr, hr_type)
        return True
    except ValidationError:
        return False


def validate_date_time(date_time):
    time_format = "%Y-%m-%d %H:%M:%S.%f"
    try:
        datetime.datetime.strptime(date_time, time_format)
        return True
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD HH:MM:SS.ssssss")
