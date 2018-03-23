from pymodm import connect
import models
import datetime
from numpy import mean

connect("mongodb://localhost:27017/heart_rate_app")  # open up connection to db


def update_user(email, age, heart_rate):
    """Updates user by detecting if user exists and either creating new user or updating existing user

        :param email: user email as string type which serves as user id
        :param age: user age as integer type
        :param heart_rate: one heart rate measurement as integer type
        :returns: updates user information in mongo database
    """
    if models.User.objects.raw({"_id": email}).count() == 0:
        create_user(email, age, heart_rate)
    else:
        add_hr(email, heart_rate)


def check_user_exists(email):
    """Check if a user exists in the mongo database by searching for their email

            :param email: user email as string type which serves as user id
            :returns: True if user exists, False if user does not exist
    """
    if models.User.objects.raw({"_id": email}).count() == 0:
        return False
    else:
        return True


def add_hr(email, heart_rate):
    """Updates existing user by adding new heart rate measurement and timestamp of measurement

        :param email: user email as string type which serves as user id
        :param heart_rate: one heart rate measurement as integer type
        :returns: adds new heart rate measurement and timestamp of measurement to mongo database
    """
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    user.heart_rate.append(heart_rate)  # Append the heart_rate to the user's list of heart rates
    user.heart_rate_times.append(datetime.datetime.now())  # append the current time to the user's list of heart rate times
    user.save()  # save the user to the database


def create_user(email, age, heart_rate):
    """Creates new user in mongo database with new heart rate measurement and timestamp

            :param email: user email as string type which serves as user id
            :param age: user age as integer type
            :param heart_rate: one heart rate measurement as integer type
            :returns: adds new user with age, heart rate measurement, and timestamp of measurement to mongo database
    """
    user = models.User(email, age, [heart_rate], [datetime.datetime.now()])  # create a new User instance
    user.save()  # save the user to the database


def get_hr_and_times(email):
    """Gets all heart rates and timestamps for a user

            :param email: user email as string type which serves as user id
            :returns: list of heart rates, list of timestamps, and age of user
    """
    user = models.User.objects.raw({"_id": email}).first()
    hr = user.heart_rate
    times = user.heart_rate_times
    age = user.age
    return hr, times, age


def check_tachy(email, avg_hr):
    """Checks if a heart rate is tachycardic based on user's age

            :param email: user email as string type which serves as user id
            :param avg_hr: one heart rate measurement as integer type
            :returns: True if heart rate is tachycardic, otherwise False
    """
    user = models.User.objects.raw({"_id": email}).first()
    age = user.age

    if age <= 2 and avg_hr > 151:
        tachy = True
    elif age in range(3, 5) and avg_hr > 137:
        tachy = True
    elif age in range(5, 8) and avg_hr > 133:
        tachy = True
    elif age in range(8, 12) and avg_hr > 130:
        tachy = True
    elif age in range(12, 16) and avg_hr > 119:
        tachy = True
    elif age >= 6 and avg_hr > 100:
        tachy = True
    else:
        tachy = False
    return tachy


def calc_avg_for_interval(email, time_since):
    """Calculates average heart rate after a certain timestamp

            :param email: user email as string type which serves as user id
            :param time_since: timestamp as string type in the format YYYY-MM-DD HH:MM:SS.ssssss
            :returns: average heart rate after the input timestamp
    """
    user = models.User.objects.raw({"_id": email}).first()
    hr = user.heart_rate
    times = user.heart_rate_times
    new_hr = []
    for i, time in enumerate(times):
        if time > time_since:
            new_hr.append(hr[i])
    avg_hr = mean(new_hr)
    return avg_hr


# if __name__ == "__main__":
#     # connect("mongodb://localhost:27017/heart_rate_app") # open up connection to db
#     create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60)  # we should only do this once, otherwise will overwrite existing user
#     add_hr("suyash@suyashkumar.com", 60, datetime.datetime.now())
#     print_user("suyash@suyashkumar.com")
