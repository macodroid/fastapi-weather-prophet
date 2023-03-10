from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import WeatherInfo
from schemas import WeatherInfoSchema


def get_info(db: Session):
    return db.query(WeatherInfo).all()


def get_info_for_today(db: Session):
    today = datetime.utcnow() + timedelta(hours=1)
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(1)
    return db.query(WeatherInfo).filter(func.date(WeatherInfo.weather_date) >= start,
                                        func.date(WeatherInfo.weather_date) < end).all()


def get_info_in_date_range(db: Session, start_date: datetime, end_date: datetime):
    return db.query(WeatherInfo).filter(func.date(WeatherInfo.weather_date) >= start_date,
                                        func.date(WeatherInfo.weather_date) < end_date).all()


def get_info_by_date(db: Session, weather_date: datetime):
    return db.query(WeatherInfo).filter(WeatherInfo.weather_date == weather_date).first()


def get_info_for_last_window_hours(db: Session, window_hours: int):
    today = datetime.utcnow() + timedelta(hours=1)
    start = datetime(today.year, today.month, today.day, today.hour) - timedelta(hours=window_hours - 1)
    end = datetime(today.year, today.month, today.day, today.hour)
    return db.query(WeatherInfo).filter(WeatherInfo.weather_date >= start,
                                        WeatherInfo.weather_date <= end).all()


def create_weather_info(db: Session, info: WeatherInfoSchema):
    _info = WeatherInfo(weather_date=info.weather_date,
                        humidity=info.humidity,
                        pressure=info.pressure,
                        wind_speed=info.wind_speed,
                        actual_temperature=info.actual_temperature,
                        temperature_baseline=info.temperature_baseline,
                        temperature_mlp=info.temperature_mlp,
                        temperature_gru=info.temperature_gru)
    db.add(_info)
    db.commit()
    db.refresh(_info)
    return _info


def update_current_weather_info(db: Session, weather_info: WeatherInfoSchema):
    _info = get_info_by_date(db=db, weather_date=weather_info.weather_date)

    _info.actual_temperature = weather_info.actual_temperature
    _info.humidity = weather_info.humidity
    _info.pressure = weather_info.pressure
    _info.wind_speed = weather_info.wind_speed

    db.commit()
    db.refresh(_info)
    return _info


def add_predicted_temperature(db: Session, weather_date: datetime,
                              temperature_baseline: float,
                              temperature_mlp: float,
                              temperature_gru: float):
    _info = WeatherInfo(weather_date=weather_date,
                        temperature_baseline=temperature_baseline,
                        temperature_mlp=temperature_mlp,
                        temperature_gru=temperature_gru)

    db.add(_info)
    db.commit()
    db.refresh(_info)
    return _info
