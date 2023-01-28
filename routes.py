from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config import SessionLocal
from sqlalchemy.orm import Session
from schemas import WeatherInfoSchema, Request, Response, RequestWeatherInfo

import crud

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

