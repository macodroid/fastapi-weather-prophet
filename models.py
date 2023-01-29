from datetime import datetime, date

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Float

from config import Base


class WeatherRange(BaseModel):
    start_date: date
    end_date: date


class WeatherInfo(Base):
    __tablename__ = 'weather_info'

    weather_date = Column(DateTime, primary_key=True, index=True)

    humidity = Column(Float)
    pressure = Column(Float)
    wind_speed = Column(Float)
    actual_temperature = Column(Float)
    temperature_baseline = Column(Float)
    temperature_mlp = Column(Float)
    temperature_gru = Column(Float)
