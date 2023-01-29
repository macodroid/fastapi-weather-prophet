from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import WeatherInfo
from schemas import WeatherInfoSchema


def get_info(db: Session):
    return db.query(WeatherInfo).all()


def get_info_for_today(db: Session):
    today = datetime.now().date()
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
    today = datetime.now().date()
    start = datetime(today.year, today.month, today.day, datetime.now().hour) - timedelta(hours=window_hours - 1)
    end = datetime(today.year, today.month, today.day, datetime.now().hour)
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


def update_actual_temperature(db: Session, weather_date: datetime, actual_temperature: float):
    _info = get_info_by_date(db=db, weather_date=weather_date)

    _info.actual_temperature = actual_temperature

    db.commit()
    db.refresh(_info)
    return _info


def update_predicted_temperature(db: Session, weather_date: datetime,
                                 temperature_baseline: float,
                                 temperature_mlp: float,
                                 temperature_gru: float):
    _info = get_info_by_date(db=db, weather_date=weather_date)

    _info.temperature_baseline = temperature_baseline
    _info.temperature_baseline = temperature_mlp
    _info.temperature_baseline = temperature_gru

    db.commit()
    db.refresh(_info)
    return _info
