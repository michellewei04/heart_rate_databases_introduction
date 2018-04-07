from flask import Flask, jsonify, request
from flask_cors import CORS
import models
from database_interface import update_user, check_tachy, calc_avg_for_interval, check_user_exists
from numpy import mean
import datetime
from validation import validate_email_format, validate_hr_input, validate_date_time_input

app = Flask(__name__)
CORS(app)


@app.route("/api/heart_rate", methods=["POST"])
def post_user():
    r = request.get_json()
    email = r["user_email"]
    if not validate_email_format(email):
        res = {
            "Message": "Email ({0}) is not in valid format".format(email)
        }
        code = 400
    elif not validate_hr_input(r):
        res = {
            "Message": "Age or heart rate not in valid format. Both must be integers greater than 0"
        }
        code = 400
    else:
        age = r["user_age"]
        hr = r["heart_rate"]
        update_user(email, age, hr)
        res = {
            "Message": "Data successfully added to database",
            "Data": r
        }
        code = 200
    return jsonify(res), code


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_hr(user_email):
    if not validate_email_format(user_email):
        res = {
            "Message": "Email ({0}) is not in valid format".format(user_email)
        }
        code = 400
    elif not check_user_exists(user_email):
        res = {
            "Message": "User ({0}) does not exist".format(user_email)
        }
        code = 400
    else:
        user = models.User.objects.raw({'_id': user_email}).first()
        hr = user.heart_rate
        times = user.heart_rate_times
        new_times = []
        for time in times:
            time = str(time)
            new_times.append(time)

        res = {
            "User heart rates and times": [hr, new_times]
        }
        code = 200
    return jsonify(res), code


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_avg_hr(user_email):
    if not validate_email_format(user_email):
        res = {
            "Message": "Email ({0}) is not in valid format".format(user_email)
        }
        code = 400
    elif not check_user_exists(user_email):
        res = {
            "Message": "User ({0}) does not exist".format(user_email)
        }
        code = 400
    else:
        user = models.User.objects.raw({'_id': user_email}).first()
        hr = user.heart_rate
        avg_hr = mean(hr)
        tachy = check_tachy(user_email, avg_hr)
        if tachy:
            res = {
                "Message": "Heart rate for {0} is considered tachycardic for user's current age".format(user_email),
                "Average heart rate": avg_hr,
            }
        else:
            res = {
                "Message": "Heart rate for {0} is considered normal".format(user_email),
                "Average heart rate": avg_hr,
            }
        code = 200
    return jsonify(res), code


@app.route("/api/heart_rate/interval_average", methods=["POST"])
def post_interval_avg():
    r = request.get_json()
    user_email = r["user_email"]
    time_since = r["heart_rate_average_since"]
    if not validate_email_format(user_email):
        res = {
            "Message": "Email ({0}) is not in valid format".format(user_email)
        }
        code = 400
    elif not check_user_exists(user_email):
        res = {
            "Message": "User ({0}) does not exist".format(user_email)
        }
        code = 400
    elif validate_date_time_input(time_since) == ValueError:
        res = {
            "Message": "heart_rate_average_since' must be in the format YYYY-MM-DD HH:MM:SS.ssssss"
        }
        code = 400
    elif validate_date_time_input(time_since) == TypeError:
        res = {
            "Message": "heart_rate_average_since' must be a string in the format YYYY-MM-DD HH:MM:SS.ssssss"
        }
        code = 400
    else:
        time_since = datetime.datetime.strptime(time_since, '%Y-%m-%d %H:%M:%S.%f')
        avg_hr = calc_avg_for_interval(user_email, time_since)
        tachy = check_tachy(user_email, avg_hr)
        if tachy:
            res = {
                "Message": "Getting heart rates for {0} starting from {1}. "
                           "Average heart rate is considered tachycardic for user's current age".format(user_email, time_since),
                "Average user heart rate": avg_hr,
            }
        else:
            res = {
                "Message": "Getting heart rates for {0} starting from {1}. "
                           "Average heart rate is normal".format(user_email, time_since),
                "Average user heart rate": avg_hr,
            }
        code = 200
    return jsonify(res), code


if __name__ == "__main__":
    app.run(host="127.0.0.1")
