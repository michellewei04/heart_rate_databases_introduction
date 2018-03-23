from pymodm import connect
import models
import datetime
from numpy import mean

connect("mongodb://localhost:27017/heart_rate_app")  # open up connection to db


def update_user(email, age, heart_rate):
    if models.User.objects.raw({"_id": email}).count() == 0:
        create_user(email, age, heart_rate)
    else:
        add_hr(email, heart_rate)


def check_user_exists(email):
    if models.User.objects.raw({"_id": email}).count() == 0:
        return False
    else:
        return True


def add_hr(email, heart_rate):
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    user.heart_rate.append(heart_rate)  # Append the heart_rate to the user's list of heart rates
    user.heart_rate_times.append(datetime.datetime.now())  # append the current time to the user's list of heart rate times
    user.save()  # save the user to the database


def create_user(email, age, heart_rate):
    user = models.User(email, age, [heart_rate], [datetime.datetime.now()])  # create a new User instance
    # u.heart_rate.append(heart_rate)  # add initial heart rate
    # u.heart_rate_times.append(datetime.datetime.now())  # add initial heart rate time
    user.save()  # save the user to the database


def get_hr_and_time(email):
    user = models.User.objects.raw({"_id": email}).first()
    hr = user.heart_rate
    times = user.heart_rate_times
    age = user.age
    return hr, times, age


def check_tachy(email, avg_hr):
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
    user = models.User.objects.raw({"_id": email}).first()
    hr = user.heart_rate
    times = user.heart_rate_times
    new_hr = []
    for i, time in enumerate(times):
        if time > time_since:
            new_hr.append(hr[i])
    avg_hr = mean(new_hr)
    return avg_hr


# def clear_user(email):
#     user = models.User.objects.raw({"_id": email}).first()
#     user.delete()


def print_user(email):
    user = models.User.objects.raw({"_id": email}).first()  # Get the first user where _id=email
    print(user.email)
    print(user.heart_rate)
    print(user.heart_rate_times)


# if __name__ == "__main__":
#     # connect("mongodb://localhost:27017/heart_rate_app") # open up connection to db
#     create_user(email="suyash@suyashkumar.com", age=24, heart_rate=60)  # we should only do this once, otherwise will overwrite existing user
#     add_hr("suyash@suyashkumar.com", 60, datetime.datetime.now())
#     print_user("suyash@suyashkumar.com")
