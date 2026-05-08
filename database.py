ACTIVITY_LABELS = ["WALKING", "RUNNING", "SITTING", "STANDING", "STAIRS"]


SENSOR_PATTERNS = {
    "WALKING": {
        "accelerometer": {"x": 0.45, "y": 0.82, "z": 9.62},
        "gyroscope": {"x": 0.08, "y": 0.14, "z": 0.03},
    },
    "RUNNING": {
        "accelerometer": {"x": 1.2, "y": 2.3, "z": 11.1},
        "gyroscope": {"x": 0.22, "y": 0.34, "z": 0.16},
    },
    "SITTING": {
        "accelerometer": {"x": 0.02, "y": 0.04, "z": 9.78},
        "gyroscope": {"x": 0.01, "y": 0.01, "z": 0.0},
    },
    "STANDING": {
        "accelerometer": {"x": -0.04, "y": 0.08, "z": 9.81},
        "gyroscope": {"x": 0.0, "y": 0.02, "z": 0.01},
    },
    "STAIRS": {
        "accelerometer": {"x": 0.8, "y": 1.4, "z": 10.35},
        "gyroscope": {"x": 0.15, "y": 0.21, "z": 0.09},
    },
}

