# core/analyzer.py
import numpy as np


def calculate_rating(criteria_data: dict) -> float:
    # 1. Веса (определенные в результате анализа)
    weights = {
        "safety": 2.5,  # Приоритет на безопасность
        "transport": 2.0,
        "ecology": 1.5,
        "education": 1.5,
        "healthcare": 1.0,
        "shopping": 0.5,
        "leisure": 0.5,
        "amenities": 0.5,
        "noise": 1.0,
        "density": 1.0
    }

    # 2. Расчет взвешенной суммы
    weighted_sum = 0
    for key, weight in weights.items():
        val = criteria_data.get(key, 0)
        # Логика: если это шум, то чем выше значение, тем хуже балл
        if key == "noise":
            weighted_sum += (10 - val) * weight
        else:
            weighted_sum += val * weight

    # 3. Приведение к шкале 1-100
    # Максимально возможная сумма баллов при весах выше = 120 (условно)
    max_possible = sum(weights.values()) * 10
    final_score = (weighted_sum / max_possible) * 100

    return round(final_score, 1)