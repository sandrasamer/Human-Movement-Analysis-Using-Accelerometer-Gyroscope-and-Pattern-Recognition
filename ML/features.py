from math import atan2, degrees, sqrt


FEATURE_NAMES = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "acc_magnitude",
    "gyro_magnitude",
    "motion_intensity",
    "tilt_degrees",
]


def magnitude(values: dict[str, float]) -> float:
    return sqrt(sum(value * value for value in values.values()))


def extract_features(accelerometer: dict[str, float], gyroscope: dict[str, float]) -> dict[str, float]:
    acc_mag = magnitude(accelerometer)
    gyro_mag = magnitude(gyroscope)
    horizontal_acc = sqrt(accelerometer["x"] ** 2 + accelerometer["y"] ** 2)

    return {
        "acc_x": accelerometer["x"],
        "acc_y": accelerometer["y"],
        "acc_z": accelerometer["z"],
        "gyro_x": gyroscope["x"],
        "gyro_y": gyroscope["y"],
        "gyro_z": gyroscope["z"],
        "acc_magnitude": round(acc_mag, 4),
        "gyro_magnitude": round(gyro_mag, 4),
        "motion_intensity": round(abs(acc_mag - 9.81) + gyro_mag * 3, 4),
        "tilt_degrees": round(degrees(atan2(horizontal_acc, abs(accelerometer["z"]) or 0.001)), 4),
    }

