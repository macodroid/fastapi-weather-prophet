from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every
from fastapi.staticfiles import StaticFiles
from starlette.responses import Response, StreamingResponse
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from datetime import datetime

import models
from forcast import weather_forcasting
from routes import router
from config import engine
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

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


# @app.get("/temperature-data")
# async def chart_data() -> StreamingResponse:
#     response = StreamingResponse(await get_fresh_weather_data(), media_type="text/event-stream")
#     response.headers["Cache-Control"] = "no-cache"
#     response.headers["X-Accel-Buffering"] = "no"
#     return response


@app.on_event("startup")
@repeat_every(seconds=10, wait_first=True)
@app.get("/temperature-data")
def get_fresh_weather_data():
    test = True
    now = datetime.now()
    if 0 <= now.minute < 3:
        print("Getting fresh weather data round hour")
        response = StreamingResponse(weather_forcasting(), media_type="text/event-stream")
        response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Accel-Buffering"] = "no"
        return response
    if test:
        print("Getting fresh weather data")
        response = StreamingResponse(weather_forcasting(), media_type="text/event-stream")
        response.headers["Cache-Control"] = "no-cache"
        response.headers["X-Accel-Buffering"] = "no"
        return response

