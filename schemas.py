from datetime import datetime
from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel , Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class WeatherInfoSchema(BaseModel):
    weather_date: datetime = None
    humidity: float = None
    pressure: float = None
    wind_speed: float = None
    actual_temperature: float = None
    temperature_baseline: float = None
    temperature_mlp: float = None
    temperature_gru: float = None

    class Config:
        orm_mode = True


class Request(GenericModel, Generic[T]):
    parameter: Optional[T] = Field(...)


class RequestWeatherInfo(BaseModel):
    parameter: WeatherInfoSchema = Field(...)


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
