from datetime import datetime

from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every

import models
from config import engine
from forcast import weather_forcasting
from routes import router

streaming = False

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/weather", tags=["weather"])


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/history", response_class=HTMLResponse)
async def index2(request: Request) -> Response:
    return templates.TemplateResponse("history.html", {"request": request})


@app.on_event("startup")
@repeat_every(seconds=90, wait_first=True)
def get_fresh_weather_data():
    now = datetime.now()
    if 0 <= now.minute < 2:
        logger.info("Forcasting new weather data")
        weather_forcasting()
