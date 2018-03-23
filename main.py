from flask import Flask, jsonify, request
import models
from database_interface import update_user, check_tachy, calc_avg_for_interval, clear_user
from numpy import mean

# app = Flask(__name__, static_url_path='/static)
app = Flask(__name__)


@app.route("/api/heart_rate", methods=["POST"])
def post_user():
    r = request.get_json()                  # need to validate type and format of email, age, hr
    email = r["user_email"]
    age = r["user_age"]
    hr = r["user_heart_rate"]
    if hr == "clear":
        clear_user(email)
        res = {
            "Message": "User {0} successfully cleared".format(email)
        }
    else:
        update_user(email, age, hr)             # update_user function from database_interface
        res = {
            "Message": "Data successfully added to database",
            "Data": r
        }
    return jsonify(res)


@app.route("/api/heart_rate/<user_email>", methods=["GET"])
def get_hr(user_email):
    user = models.User.objects.raw({'_id': user_email}).first()
    hr = user.heart_rate
    times = user.heart_rate_times
    res = {
        "User heart rates and times": [hr, times]
    }
    return jsonify(res)


@app.route("/api/heart_rate/average/<user_email>", methods=["GET"])
def get_avg_hr(user_email):
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
    return jsonify(res)


@app.route("/interval_average", methods=["POST"])
def post_interval_avg():
    r = request.get_json()                          # need to validate email and time format
    user_email = r["user_email"]
    time_since = r["heart_rate_average_since"]
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
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="127.0.0.1")
