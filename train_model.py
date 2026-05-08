import json
from datetime import datetime
from pathlib import Path
from random import Random

from app.ML.features import FEATURE_NAMES, extract_features
from app.database import ACTIVITY_LABELS, SENSOR_PATTERNS


MODEL_PATH = Path(__file__).resolve().parent / "model" / "har_model.json"
RNG = Random(304)


def jitter(values: dict[str, float], spread: float) -> dict[str, float]:
    return {axis: round(value + RNG.uniform(-spread, spread), 4) for axis, value in values.items()}


def build_dataset(samples_per_class: int = 160) -> list[dict]:
    rows = []
    for label in ACTIVITY_LABELS:
        pattern = SENSOR_PATTERNS[label]
        for _ in range(samples_per_class):
            features = extract_features(
                jitter(pattern["accelerometer"], 0.22),
                jitter(pattern["gyroscope"], 0.05),
            )
            rows.append({"label": label, "features": features})
    return rows


def centroid(rows: list[dict]) -> dict[str, float]:
    return {
        feature: round(sum(row["features"][feature] for row in rows) / len(rows), 5)
        for feature in FEATURE_NAMES
    }


def distance(left: dict[str, float], right: dict[str, float]) -> float:
    weights = {
        "acc_magnitude": 1.6,
        "gyro_magnitude": 2.4,
        "motion_intensity": 2.0,
        "tilt_degrees": 0.08,
    }
    return sum(weights.get(feature, 1.0) * abs(left[feature] - right[feature]) for feature in FEATURE_NAMES)


def evaluate(rows: list[dict], centroids: dict[str, dict[str, float]]) -> tuple[float, dict[str, dict[str, int]]]:
    confusion = {actual: {predicted: 0 for predicted in ACTIVITY_LABELS} for actual in ACTIVITY_LABELS}
    correct = 0

    for row in rows:
        prediction = min(
            ACTIVITY_LABELS,
            key=lambda label: distance(row["features"], centroids[label]),
        )
        confusion[row["label"]][prediction] += 1
        correct += int(prediction == row["label"])

    return round(correct / len(rows), 4), confusion


def main() -> None:
    rows = build_dataset()
    centroids = {
        label: centroid([row for row in rows if row["label"] == label])
        for label in ACTIVITY_LABELS
    }
    accuracy, confusion_matrix = evaluate(rows, centroids)

    MODEL_PATH.parent.mkdir(exist_ok=True)
    MODEL_PATH.write_text(
        json.dumps(
            {
                "model_name": "Trained Centroid HAR Classifier",
                "source": "Synthetic mobile accelerometer/gyroscope training set",
                "trained_at": datetime.now().isoformat(timespec="seconds"),
                "samples": len(rows),
                "accuracy": accuracy,
                "features": FEATURE_NAMES,
                "classes": ACTIVITY_LABELS,
                "centroids": centroids,
                "confusion_matrix": confusion_matrix,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"Saved {MODEL_PATH}")
    print(f"Training accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    main()

