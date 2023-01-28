from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from starlette.responses import Response
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from datetime import datetime

import models
from forcast import weather_forcasting, get_window_weather_data
from routes import router
from config import engine
from fastapi.requests import Request

templates = Jinja2Templates(directory="templates")
print("Creating database")
models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


app.include_router(router, prefix="/weather", tags=["weather"])


@app.on_event("startup")
def load_models():
    # TODO somehow we need to load model on startup
    pass


@app.on_event("startup")
@repeat_every(seconds=2, wait_first=True)
def get_fresh_weather_data():
    test = True
    now = datetime.now()
    if 0 <= now.minute > 3:
        print("Getting fresh weather data")
        weather_forcasting()
    if test:
        weather_forcasting()
