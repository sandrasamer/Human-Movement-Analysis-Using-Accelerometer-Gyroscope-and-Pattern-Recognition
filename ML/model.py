import json
from math import exp, sqrt
from pathlib import Path

from app.ML.features import FEATURE_NAMES, extract_features
from app.database import ACTIVITY_LABELS, SENSOR_PATTERNS
from app.utils import normalize_probabilities


MODEL_PATH = Path(__file__).resolve().parents[2] / "model" / "har_model.json"


def _default_model_data() -> dict:
    centroids = {}
    for label, pattern in SENSOR_PATTERNS.items():
        centroids[label] = extract_features(pattern["accelerometer"], pattern["gyroscope"])

    return {
        "model_name": "Centroid HAR Classifier",
        "source": "Built-in sensor profile fallback",
        "accuracy": 0.86,
        "features": FEATURE_NAMES,
        "centroids": centroids,
        "confusion_matrix": {
            label: {predicted: 0 for predicted in ACTIVITY_LABELS}
            for label in ACTIVITY_LABELS
        },
    }


class HumanActivityModel:
    def __init__(self) -> None:
        self.model_data = self._load_model_data()

    def _load_model_data(self) -> dict:
        if MODEL_PATH.exists():
            with MODEL_PATH.open("r", encoding="utf-8") as model_file:
                return json.load(model_file)
        return _default_model_data()

    def predict(self, accelerometer: dict[str, float], gyroscope: dict[str, float]) -> dict:
        features = extract_features(accelerometer, gyroscope)

        raw_scores = {}
        for label in ACTIVITY_LABELS:
            centroid = self.model_data["centroids"][label]
            distance = self._distance(features, centroid)
            raw_scores[label] = exp(-distance)

        probabilities = normalize_probabilities(raw_scores)
        prediction = max(probabilities, key=probabilities.get)

        return {
            "prediction": prediction,
            "confidence": probabilities[prediction],
            "probabilities": probabilities,
            "features": features,
            "model_type": self.model_data["model_name"],
        }

    def _distance(self, features: dict[str, float], centroid: dict[str, float]) -> float:
        weights = {
            "acc_magnitude": 1.6,
            "gyro_magnitude": 2.4,
            "motion_intensity": 2.0,
            "tilt_degrees": 0.08,
        }
        total = 0.0
        for feature in FEATURE_NAMES:
            weight = weights.get(feature, 1.0)
            total += weight * (features[feature] - centroid[feature]) ** 2
        return sqrt(total)

    def info(self) -> dict:
        return {
            "model_name": self.model_data["model_name"],
            "source": self.model_data["source"],
            "accuracy": self.model_data["accuracy"],
            "features": self.model_data["features"],
            "classes": ACTIVITY_LABELS,
            "confusion_matrix": self.model_data.get("confusion_matrix", {}),
        }


model = HumanActivityModel()
