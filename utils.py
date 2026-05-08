from math import sqrt


def magnitude(values: dict[str, float]) -> float:
    return sqrt(sum(value * value for value in values.values()))


def normalize_probabilities(scores: dict[str, float]) -> dict[str, float]:
    total = sum(scores.values()) or 1
    return {label: round(score / total, 3) for label, score in scores.items()}

