from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests
import torch
from fastapi.logger import logger

import config
import crud
import utils as helper
from config import SessionLocal
from schemas import WeatherInfoSchema

# loading data just once
device = torch.device('cpu')
data_mean, data_std = np.load('data/stat.npy')
mlp_model = torch.jit.load('ml_models/mlp_jit_L1.pt', map_location=device)
mlp_model.eval()
gru_model = torch.jit.load('ml_models/gru_jit_128_4_L1_final.pt', map_location=device)
gru_model.eval()
envs = config.Settings()


# we will not stream data to frontend. Instead we will insert data to database
# def stream_weather_data():
#     data = weather_forcasting()
#     if data is None:
#         return
#     stream_data = json.dumps(
#         {
#             "actual_temperature": data["actual_temperature"],
#             "baseline_temperature": data["baseline_temperature"],
#             "mlp_temperature": data["mlp_temperature"],
#             "gru_temperature": data["gru_temperature"],
#             "weather_date": data["weather_date"]
#         })
#     yield f"data:{stream_data}\n\n"


# TODO insert data to database
def weather_forcasting():
    db = SessionLocal()
    date = datetime.utcnow() + timedelta(hours=1)
    current_weather_date = datetime(date.year, date.month, date.day, date.hour)
    weather_date_one_hour_ahead = current_weather_date + timedelta(hours=1)
    try:
        act_temperature = get_openweather_data(db, weather_date=current_weather_date)
        window_weather_info = get_window_weather_data(db)
        weather_features = helper.process_weather_data(window_weather_info)
        baseline_prediction = baseline_temperature_prediction(weather_features)
        norm_weather_features = np.array((weather_features - data_mean) / data_std)
        mlp_prediction = mlp_temperature_prediction(norm_weather_features)
        gru_prediction = gru_temperature_prediction(norm_weather_features)
        logger.info(
            f"Creating new row with predictions: "
            f"{baseline_prediction}, {mlp_prediction}, {gru_prediction} for date: {weather_date_one_hour_ahead}.")
        add_temperature_prediction(db, weather_date_one_hour_ahead, baseline_prediction, mlp_prediction,
                                   gru_prediction)
        logger.info("New record with predictions was created.")
        db.close()
        return {
            "actual_temperature": act_temperature,
            "baseline_temperature": baseline_prediction,
            "mlp_temperature": mlp_prediction,
            "gru_temperature": gru_prediction,
        }
    except Exception as e:
        print(e)


def get_openweather_data(db_session: SessionLocal, weather_date: datetime):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?" \
              f"lat=48.171704276327475&lon=17.211020714029374&units=metric&appid={envs.OPEN_WEATHER_API_KEY}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        weather_info = WeatherInfoSchema()
        weather_info.weather_date = weather_date
        weather_info.actual_temperature = response.json()["main"]["temp"]
        weather_info.humidity = response.json()["main"]["humidity"]
        # convert form hPa to mmHg
        weather_info.pressure = response.json()["main"]["pressure"] * 0.75006156130264
        weather_info.wind_speed = response.json()["wind"]["speed"]
        logger.info("Updating current weather info: ", weather_info.weather_date, " with values: humidity: ",
                    weather_info.humidity, " pressure: ", weather_info.pressure, " wind speed: ",
                    weather_info.wind_speed,
                    " actual temperature: ", weather_info.actual_temperature)
        update_current_weather_info(db_session, weather_info=weather_info)
        logger.info("Successfully current weather info.")
        return weather_info.actual_temperature
    except Exception as e:
        logger.exception(e)


def insert_actual_temperature(db_session: SessionLocal, weather_info: WeatherInfoSchema):
    try:
        crud.create_weather_info(db_session, info=weather_info)
    except Exception as e:
        logger.exception(e)


def update_current_weather_info(db_session: SessionLocal, weather_info: WeatherInfoSchema):
    try:
        crud.update_current_weather_info(db_session, weather_info=weather_info)
    except Exception as e:
        logger.exception(e)


def get_window_weather_data(db_session: SessionLocal):
    try:
        return crud.get_info_for_last_window_hours(db_session, window_hours=6)
    except Exception as e:
        logger.exception(e)


def baseline_temperature_prediction(weather_info: pd.DataFrame):
    baseline_prediction = weather_info["actual_temperature"].mean() + 1
    return baseline_prediction


def mlp_temperature_prediction(weather_features: np.array):
    features = np.reshape(weather_features, (1, 6, 8))
    features = torch.from_numpy(features).float().to(device)
    prediction = mlp_model(features)
    return float(prediction.detach().numpy()[0][0][0])


def gru_temperature_prediction(weather_features: np.array):
    features = np.reshape(weather_features, (1, 6, 8))
    features = torch.from_numpy(features).float().to(device)
    h0 = torch.zeros(2, 6, 128).to(device)
    prediction = gru_model(features, h0)
    return float(prediction.detach().numpy()[0][0])


def add_temperature_prediction(db_session: SessionLocal, weather_date, baseline, mlp, gru):
    try:
        crud.add_predicted_temperature(db_session, weather_date, baseline, mlp, gru)
    except Exception as e:
        logger.exception(e)
