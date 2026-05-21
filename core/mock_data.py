"""
Mock-данные районов с приблизительными полигонами границ.
Полигоны строятся как многоугольники вокруг центра района, чтобы
карта выглядела наглядно. Для продакшна сюда стоит подгрузить
настоящие границы из OpenStreetMap (Overpass API).
"""

import math


def _polygon_around(lat, lon, radius_km=1.2, sides=8, jitter=0.15, seed=0):
    """Возвращает координаты простого полигона (массив [lon, lat]) вокруг точки."""
    coords = []
    # широта: 1 градус ≈ 111 км; долгота: зависит от широты
    dlat = radius_km / 111.0
    dlon = radius_km / (111.0 * math.cos(math.radians(lat)))
    for i in range(sides):
        angle = 2 * math.pi * i / sides
        # детерминированное "дрожание" формы, чтобы полигоны не были идеальными кругами
        wobble = 1 + jitter * math.sin(angle * 3 + seed)
        x = lon + dlon * math.cos(angle) * wobble
        y = lat + dlat * math.sin(angle) * wobble
        coords.append([x, y])
    coords.append(coords[0])  # замыкаем кольцо
    return {"type": "Polygon", "coordinates": [coords]}


# Базовые данные: имя, центр (lat, lon), радиус, базовые оценки 1–10
MOSCOW = [
    ("Тверской",        55.7650, 37.6050, 1.2, {"transport": 9.5, "education": 8.8, "healthcare": 8.5, "ecology": 4.2, "safety": 6.5, "shopping": 9.8, "leisure": 9.6, "amenities": 9.0, "noise": 3.0, "density": 2.5}),
    ("Хамовники",       55.7300, 37.5800, 1.3, {"transport": 8.8, "education": 9.2, "healthcare": 8.7, "ecology": 6.5, "safety": 8.0, "shopping": 8.5, "leisure": 9.0, "amenities": 8.7, "noise": 5.5, "density": 5.0}),
    ("Арбат",           55.7500, 37.5900, 1.0, {"transport": 9.0, "education": 8.5, "healthcare": 8.0, "ecology": 5.0, "safety": 7.0, "shopping": 9.5, "leisure": 9.7, "amenities": 9.2, "noise": 3.5, "density": 3.0}),
    ("Замоскворечье",   55.7370, 37.6300, 1.2, {"transport": 8.7, "education": 8.0, "healthcare": 7.8, "ecology": 5.5, "safety": 7.5, "shopping": 8.8, "leisure": 8.5, "amenities": 8.5, "noise": 4.5, "density": 4.0}),
    ("Раменки",         55.7050, 37.5000, 1.8, {"transport": 7.5, "education": 8.7, "healthcare": 7.5, "ecology": 8.5, "safety": 8.2, "shopping": 7.0, "leisure": 7.5, "amenities": 7.8, "noise": 7.5, "density": 6.5}),
    ("Ясенево",         55.6050, 37.5300, 2.0, {"transport": 6.5, "education": 7.5, "healthcare": 7.0, "ecology": 8.8, "safety": 7.5, "shopping": 6.5, "leisure": 6.0, "amenities": 6.5, "noise": 8.0, "density": 7.0}),
    ("Митино",          55.8450, 37.3600, 2.2, {"transport": 6.0, "education": 7.0, "healthcare": 6.8, "ecology": 8.0, "safety": 7.8, "shopping": 7.0, "leisure": 6.2, "amenities": 7.0, "noise": 7.5, "density": 6.8}),
    ("Бирюлёво Восточное", 55.5900, 37.6900, 1.8, {"transport": 4.5, "education": 5.5, "healthcare": 5.0, "ecology": 4.5, "safety": 4.0, "shopping": 5.5, "leisure": 4.5, "amenities": 5.0, "noise": 6.0, "density": 5.5}),
    ("Капотня",         55.6350, 37.7900, 1.5, {"transport": 4.0, "education": 5.0, "healthcare": 4.5, "ecology": 2.0, "safety": 4.5, "shopping": 4.5, "leisure": 4.0, "amenities": 4.5, "noise": 4.0, "density": 6.0}),
    ("Сокольники",      55.7900, 37.6700, 1.6, {"transport": 8.0, "education": 7.5, "healthcare": 7.5, "ecology": 8.5, "safety": 7.8, "shopping": 7.5, "leisure": 9.0, "amenities": 8.0, "noise": 7.5, "density": 6.0}),
]

SPB = [
    ("Центральный",     59.9340, 30.3520, 1.5, {"transport": 9.3, "education": 9.0, "healthcare": 8.5, "ecology": 4.5, "safety": 6.8, "shopping": 9.5, "leisure": 9.8, "amenities": 9.2, "noise": 3.5, "density": 2.8}),
    ("Адмиралтейский",  59.9200, 30.3050, 1.4, {"transport": 9.0, "education": 8.5, "healthcare": 8.0, "ecology": 5.0, "safety": 7.0, "shopping": 9.0, "leisure": 9.5, "amenities": 9.0, "noise": 4.0, "density": 3.5}),
    ("Петроградский",   59.9650, 30.3100, 1.6, {"transport": 8.5, "education": 8.8, "healthcare": 8.2, "ecology": 7.0, "safety": 8.0, "shopping": 8.5, "leisure": 9.0, "amenities": 8.7, "noise": 5.5, "density": 5.0}),
    ("Василеостровский", 59.9450, 30.2700, 1.7, {"transport": 7.8, "education": 9.2, "healthcare": 8.0, "ecology": 7.5, "safety": 8.2, "shopping": 8.0, "leisure": 8.5, "amenities": 8.5, "noise": 6.0, "density": 5.5}),
    ("Выборгский",      60.0250, 30.3550, 2.5, {"transport": 7.0, "education": 8.0, "healthcare": 7.5, "ecology": 8.0, "safety": 7.5, "shopping": 7.5, "leisure": 7.0, "amenities": 7.5, "noise": 7.0, "density": 6.5}),
    ("Приморский",      60.0050, 30.2550, 2.8, {"transport": 6.5, "education": 7.8, "healthcare": 7.2, "ecology": 8.5, "safety": 8.0, "shopping": 7.8, "leisure": 7.5, "amenities": 7.8, "noise": 7.5, "density": 6.8}),
    ("Фрунзенский",     59.8650, 30.3700, 2.2, {"transport": 6.8, "education": 7.0, "healthcare": 6.8, "ecology": 6.5, "safety": 6.5, "shopping": 7.0, "leisure": 6.5, "amenities": 6.8, "noise": 6.5, "density": 5.5}),
    ("Невский",         59.9100, 30.4500, 2.5, {"transport": 7.2, "education": 6.8, "healthcare": 6.5, "ecology": 5.5, "safety": 6.0, "shopping": 7.2, "leisure": 6.8, "amenities": 6.5, "noise": 5.5, "density": 5.8}),
    ("Кировский",       59.8800, 30.2700, 2.4, {"transport": 6.5, "education": 6.5, "healthcare": 6.2, "ecology": 5.0, "safety": 6.0, "shopping": 6.5, "leisure": 6.0, "amenities": 6.2, "noise": 5.5, "density": 5.8}),
    ("Красногвардейский", 59.9800, 30.4500, 2.6, {"transport": 6.0, "education": 6.5, "healthcare": 6.0, "ecology": 6.5, "safety": 6.5, "shopping": 6.5, "leisure": 5.8, "amenities": 6.2, "noise": 6.5, "density": 6.0}),
]


def build_city(city_name, raw_data):
    out = []
    for idx, (name, lat, lon, radius, criteria) in enumerate(raw_data):
        geometry = _polygon_around(lat, lon, radius_km=radius, sides=10, jitter=0.18, seed=idx)
        out.append({
            "name": name,
            "city": city_name,
            "lat": lat,
            "lon": lon,
            "geometry": geometry,
            "criteria": criteria,
        })
    return out


def all_districts():
    return build_city("Moscow", MOSCOW) + build_city("Saint-Petersburg", SPB)
