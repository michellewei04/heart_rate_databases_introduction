# Heart rate database and web server

[![Build Status](https://travis-ci.org/michellewei04/heart_rate_databases_introduction.svg?branch=master)](https://travis-ci.org/michellewei04/heart_rate_databases_introduction)

Contributors: Michelle Wei

Description: This is a web service for handling heart rate data. It uses a MongoDB database running in a Docker container

## Instructions

Before using, make sure MongoDB and Docker are installed. Launch the database on your local machine:
```python
docker run -v $PWD/db:/data/db -p 127.0.0.1:27017:27017 mongo
```
Run the server:
```python
gunicorn --bind 0.0.0.0:5000 main:app
```

The database hold users emails, age, heart rates, and the time of heart rate measurement. Users are identified with their unique emails.

1. To add a user and their heart rate, or add a heart rate measurement to an existing user, `POST /api/heart_rate` with
```python
{
    "user_email": "suyash@suyashkumar.com",
    "user_age": 50, // in years
    "heart_rate": 100
}
```
2. To return all heart rate measurements and time stamps for a user, `GET /api/heart_rate/<user_email>`
3. To return a user's average heart rate over all measurements, `GET /api/heart_rate/average/<user_email>`
  * This will also notify you in `"messages"` if the average heart rate is tachychardic for the user's age
4. To return a user's average heart rate since a certain time, `POST /api/heart_rate/interval_average` with
```python
{
    "user_email": "suyash@suyashkumar.com",
    "heart_rate_average_since": "2018-03-09 11:00:36.372339" // date string
}
```
in which `heart_rate_average_since` must be in the format `YYYY-MM-DD HH:MM:SS.ssssss
  * This will also notify you in `"messages"` if the average heart rate is tachychardic for the user's age
  



