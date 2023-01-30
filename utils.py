import numpy as np
import pandas as pd


def process_weather_data(weather_info: list):
    weather_data = get_df_weather_data(weather_info)
    feature = create_features(weather_data)
    return feature


def get_df_weather_data(weather_info: list):
    weather_data = []
    for info in weather_info:
        data = {"weather_date": info.weather_date, "humidity": info.humidity, "pressure": info.pressure,
                "wind_speed": info.wind_speed, "actual_temperature": info.actual_temperature}
        weather_data.append(data)
    weather_df = pd.DataFrame(weather_data)
    weather_df.sort_values(by='weather_date', inplace=True)
    return pd.DataFrame(weather_data)


def create_features(weather_data: pd.DataFrame):
    weather_data.sort_values(by='weather_date', inplace=True)
    weather_data = add_day_of_year(weather_data)
    weather_data = add_time_columns(weather_data)
    weather_data = encode_cyclic_data(weather_data)
    weather_data = clean_dataframe(weather_data)
    weather_data = weather_data[
        [
            "sin_day_of_year",
            "cos_day_of_year",
            "sin_hour",
            "cos_hour",
            "pressure",
            "actual_temperature",
            "humidity",
            "wind_speed",
        ]
    ]
    return weather_data


def add_day_of_year(weather_data: pd.DataFrame) -> pd.DataFrame:
    weather_data["day_of_year"] = weather_data["weather_date"].dt.dayofyear
    return weather_data


def add_time_columns(weather_data: pd.DataFrame) -> pd.DataFrame:
    weather_data["time"] = pd.to_datetime(
        weather_data["weather_date"], format="%H:%M:%S"
    ).dt.time
    weather_data["time"] = weather_data["time"].astype("string")
    weather_data[["hour", "minutes", "seconds"]] = weather_data["time"].str.split(
        ":", expand=True
    )
    weather_data[["hour", "minutes", "seconds"]] = weather_data[
        ["hour", "minutes", "seconds"]
    ].astype(int)
    return weather_data


def get_hourly_data(weather_data: pd.DataFrame) -> pd.DataFrame:
    hourly_weather = weather_data[weather_data["minutes"] == 0]
    return hourly_weather


def clean_dataframe(weather_data: pd.DataFrame) -> pd.DataFrame:
    weather_data.drop(
        ["weather_date", "time", "minutes", "seconds", "hour", "day_of_year"],
        axis=1,
        inplace=True,
    )
    return weather_data


def encode_cyclic_data(weather_data: pd.DataFrame) -> pd.DataFrame:
    weather_data["sin_day_of_year"] = np.sin(
        2 * np.pi * weather_data["day_of_year"] / 365
    )
    weather_data["cos_day_of_year"] = np.cos(
        2 * np.pi * weather_data["day_of_year"] / 365
    )
    weather_data["sin_hour"] = np.sin(2 * np.pi * weather_data["hour"] / 24)
    weather_data["cos_hour"] = np.cos(2 * np.pi * weather_data["hour"] / 24)
    return weather_data


def normalize_data(weather_data: pd.DataFrame, mean: float = None, std: float = None):
    weather_data -= mean
    weather_data /= std
    return weather_data
