# heart rate calculations
from numpy import mean
from database_interface import get_hr_and_times



def check_tachy(avg_hr, age):
    if age <= 2 & avg_hr > 151:
        tachy = True
    elif age >= 3 & age <= 4 & avg_hr > 137:
        tachy = True
    elif age >= 5 & age <= 7 & avg_hr > 133:
        tachy = True
    elif age >= 8 & age <= 11 & avg_hr > 130:
        tachy = True
    elif age >= 12 & age <= 15 & avg_hr > 119:
        tachy = True
    elif age >= 6 & avg_hr > 100:
        tachy = True
    else:
        tachy = False
    return tachy


def calc_avg_for_interval(email, time_since, age):
    hr, times = get_hr_and_times(email)
    new_hr = []
    for i, time in enumerate(times):
        if time > time_since:
            new_hr.append(hr[i])
    avg_hr = mean(new_hr)
    return avg_hr, age

