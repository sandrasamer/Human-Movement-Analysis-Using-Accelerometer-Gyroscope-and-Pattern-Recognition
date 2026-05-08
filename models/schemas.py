from pydantic import BaseModel, Field


class AxisValues(BaseModel):
    x: float = Field(..., description="X axis value")
    y: float = Field(..., description="Y axis value")
    z: float = Field(..., description="Z axis value")


class PredictionRequest(BaseModel):
    mode: str = "RANDOM"
    accelerometer: AxisValues
    gyroscope: AxisValues


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    probabilities: dict[str, float]
    features: dict[str, float] | None = None
    model_type: str | None = None
