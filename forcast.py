from datetime import datetime

import crud
from config import SessionLocal
import requests
import numpy as np
import utils as helper

from schemas import WeatherInfoSchema

# loading data just once
data_mean, data_std = np.load('data/stat.npy')


def weather_forcasting():
    db = SessionLocal()
    try:
        # get_openweather_data(db)
        window_weather_info = get_window_weather_data(db)
        weather_info = helper.process_weather_data(window_weather_info)
        feature = np.asarray(weather_info)

        db.close()
    except Exception as e:
        print(e)


def get_openweather_data(db_session: SessionLocal):
    try:
        url = "https://api.openweathermap.org/data/2.5/weather?lat=48.171704276327475&lon=17.211020714029374&units=metric&appid=3ae431bd06e079d061c5dd76a9ee5dbc"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        weather_info = WeatherInfoSchema()
        date = datetime.now()
        weather_info.weather_date = datetime(date.year, date.month, date.day, date.hour)
        weather_info.actual_temperature = response.json()["main"]["temp"]
        weather_info.humidity = response.json()["main"]["humidity"]
        weather_info.pressure = response.json()["main"]["pressure"]
        weather_info.wind_speed = response.json()["wind"]["speed"]
        insert_actual_temperature(db_session, weather_info)
    except Exception as e:
        print(e)


def insert_actual_temperature(db_session: SessionLocal, weather_info: WeatherInfoSchema):
    try:
        crud.create_weather_info(db_session, info=weather_info)
    except Exception as e:
        print(e)


def get_window_weather_data(db_session: SessionLocal):
    try:
        return crud.get_info_for_last_window_hours(db_session, window_hours=6)
    except Exception as e:
        print(e)


def create_temperature_prediction_baseline(weather_info: np.array):
    pass


def create_temperature_prediction_mlp():
    pass


def create_temperature_prediction_gru():
    pass
