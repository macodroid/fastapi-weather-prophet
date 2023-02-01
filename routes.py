from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

import crud
from config import SessionLocal
from models import WeatherRange
from schemas import Response, RequestWeatherInfo

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all")
async def get_all_info(db: Session = Depends(get_db)):
    _info = crud.get_info(db)
    return Response(status="Ok", code="200", message="Success fetch all data", result=_info)


@router.get("/today")
async def get_info_for_today(db: Session = Depends(get_db)):
    _info = crud.get_info_for_today(db)
    _info = sorted(_info, key=lambda x: x.weather_date)
    return Response(status="Ok", code="200", message="Success fetch data for today", result=_info)


@router.post("/history")
async def get_historical_info(request: WeatherRange, db: Session = Depends(get_db)):
    start_date = datetime(request.start_date.year, request.start_date.month, request.start_date.day, 0, 0, 0)
    end_date = datetime(request.end_date.year, request.end_date.month, request.end_date.day, 23, 59, 59)
    _info = crud.get_info_in_date_range(db, start_date=start_date, end_date=end_date)
    _info = sorted(_info, key=lambda x: x.weather_date)
    return Response(status="Ok", code="200", message="Success fetch data for today", result=_info)


@router.post("/create")
async def add_weather_info(request: RequestWeatherInfo, db: Session = Depends(get_db)):
    crud.create_weather_info(db, info=request.parameter)
    return Response(status="Ok",
                    code="200",
                    message="Book created successfully").dict(exclude_none=True)


@router.patch("/update/actual_temperature")
async def update_info_actual_temperature(request: RequestWeatherInfo, db: Session = Depends(get_db)):
    _info = crud.update_actual_temperature(db, weather_date=request.parameter.weather_date,
                                           actual_temperature=request.parameter.actual_temperature)
    return Response(status="Ok", code="200", message="Success update data", result=_info)


@router.patch("/update/predicted_temperature")
async def update_info_predicted_temperature(request: RequestWeatherInfo, db: Session = Depends(get_db)):
    _info = crud.update_predicted_temperature(db, weather_date=request.parameter.weather_date,
                                              temperature_baseline=request.parameter.temperature_baseline,
                                              temperature_mlp=request.parameter.temperature_mlp,
                                              temperature_gru=request.parameter.temperature_gru)
    return Response(status="Ok", code="200", message="Success update data", result=_info)
