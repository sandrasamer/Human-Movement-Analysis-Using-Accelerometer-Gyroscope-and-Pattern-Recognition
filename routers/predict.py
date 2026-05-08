from random import choice, uniform

from fastapi import APIRouter

from app.ML.model import model
from app.database import ACTIVITY_LABELS, SENSOR_PATTERNS
from app.models.schemas import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/api", tags=["prediction"])


def jitter(values: dict[str, float], spread: float) -> dict[str, float]:
    return {axis: round(value + uniform(-spread, spread), 2) for axis, value in values.items()}


@router.get("/simulate")
async def simulate(mode: str = "RANDOM"):
    activity = choice(ACTIVITY_LABELS) if mode.upper() == "RANDOM" else mode.upper()
    pattern = SENSOR_PATTERNS.get(activity, SENSOR_PATTERNS["WALKING"])

    return {
        "mode": activity,
        "accelerometer": jitter(pattern["accelerometer"], 0.18),
        "gyroscope": jitter(pattern["gyroscope"], 0.04),
    }


@router.post("/predict", response_model=PredictionResponse)
async def predict(payload: PredictionRequest):
    return model.predict(
        payload.accelerometer.model_dump(),
        payload.gyroscope.model_dump(),
    )


@router.get("/model-info")
async def model_info():
    return model.info()
