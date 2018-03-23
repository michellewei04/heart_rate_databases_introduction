import pytest


from validation import validate_email_format, validate_hr_input, validate_date_time_input


def test_validate_email():
    email_test_cases = [("suyash@suyashkumar.com", True),
                        ("suyash123@gmail.com", True),
                        ("suyash", False),
                        ("suyash123", False),
                        ("suyash.com", False),
                        ]
    for case in email_test_cases:
        assert validate_email_format(case[0]) == case[1]


def test_validate_hr_input():
    hr_input_test_cases = [({"user_email": "a@b.c", "user_age": 20, "heart_rate": 80}, True),
                           ({"user_email": "a@b.c", "user_age": -1, "heart_rate": 80}, False),
                           ({"user_email": "a@b.c", "user_age": 1.2, "heart_rate": 80}, False),
                           ({"user_email": "a@b.c", "user_age": 20, "heart_rate": -4}, False),
                           ({"user_email": "a@b.c", "user_age": 20, "heart_rate": 342.5}, False),
                           ({"user_email": "a@b.c", "user_age": 20, "heart_rate": 342.5}, False),
                           ({"user_email": "a@b.c", "user_age": "20", "heart_rate": 80}, False),
                           ({"user_email": "a@b.c", "user_age": 20, "heart_rate": "80"}, False)
                           ]
    for case in hr_input_test_cases:
        assert validate_hr_input(case[0]) == case[1]


def test_validate_date_time_input():
    time_input_test_cases = [("2018-03-23 02:04:32.847367", True),
                             ("2018-03-23 02:04:32", ValueError),
                             ("2018-3-23", ValueError),
                             ("Fri 3/23/18 2:04", ValueError),
                             (32318, TypeError),
                             ([32318], TypeError)
                             ]
    for case in time_input_test_cases:
        assert validate_date_time_input(case[0]) == case[1]
