"""
Загружает реальные границы районов из локальных GeoJSON-файлов
(полученных на основе данных OpenStreetMap, репозиторий
codeforamerica/click_that_hood, лицензия ODbL).

На основе названия района детерминированно генерируются оценки
по 10 критериям, чтобы при перезапусках цвета и баллы не «прыгали».
В реальном проекте сюда нужно подставить парсинг настоящих данных
(метро, школы, парки, статистика преступности и т.д.).
"""

import json
import os
import random
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

CITY_FILES = {
    "Moscow": "moscow.geojson",
    "Saint-Petersburg": "spb.geojson",
}


def _polygon_rings(geom):
    """Возвращает список колец координат для Polygon / MultiPolygon."""
    if not geom:
        return []
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    if geom["type"] == "MultiPolygon":
        rings = []
        for poly in geom["coordinates"]:
            rings.extend(poly)
        return rings
    return []


def _centroid(geom):
    """Грубый центроид как среднее по bounding box внешних колец."""
    xs, ys = [], []
    for ring in _polygon_rings(geom):
        for lon, lat in ring:
            xs.append(lon)
            ys.append(lat)
    if not xs:
        return 0.0, 0.0
    return (sum(ys) / len(ys), sum(xs) / len(xs))  # lat, lon


def _clean_name(name):
    """Приводит названия типа 'район Восточный' / 'Обручевский район' к компактной форме."""
    if not name:
        return name
    n = re.sub(r"^район\s+", "", name, flags=re.IGNORECASE)
    n = re.sub(r"\s+район$", "", n, flags=re.IGNORECASE)
    n = re.sub(r"\s+муниципальный округ$", "", n, flags=re.IGNORECASE)
    n = re.sub(r"^муниципальный округ\s+", "", n, flags=re.IGNORECASE)
    n = re.sub(r"^посёлок\s+", "", n, flags=re.IGNORECASE)
    return n.strip()


# Веса по широте — центральные районы получают чуть выше оценки
# инфраструктуры/транспорта, окраины — экологии/тишины.
def _generate_criteria(name, lat, lon, city_center):
    rng = random.Random(f"{name}-{round(lat,3)}-{round(lon,3)}")

    clat, clon = city_center
    # Расстояние от центра города в "условных километрах"
    import math
    dlat = (lat - clat) * 111.0
    dlon = (lon - clon) * 111.0 * math.cos(math.radians(clat))
    dist = math.hypot(dlat, dlon)
    centrality = max(0.0, 1.0 - dist / 25.0)  # 1 в центре, 0 на 25+ км

    def jitter(mid, spread):
        return max(1.0, min(10.0, mid + rng.uniform(-spread, spread)))

    return {
        "transport":  jitter(4 + 5 * centrality, 1.5),
        "education":  jitter(5 + 3 * centrality, 1.8),
        "healthcare": jitter(5 + 3 * centrality, 1.8),
        "ecology":    jitter(4 + 5 * (1 - centrality), 1.7),
        "safety":     jitter(6, 2.2),
        "shopping":   jitter(5 + 4 * centrality, 1.5),
        "leisure":    jitter(5 + 3 * centrality, 1.8),
        "amenities":  jitter(5 + 3 * centrality, 1.6),
        "noise":      jitter(4 + 5 * (1 - centrality), 1.8),
        "density":    jitter(4 + 5 * (1 - centrality), 1.8),
    }


CITY_CENTERS = {
    "Moscow": (55.7558, 37.6176),
    "Saint-Petersburg": (59.9343, 30.3351),
}


def _load_city(city_name):
    path = os.path.join(DATA_DIR, CITY_FILES[city_name])
    with open(path, encoding="utf-8") as f:
        gj = json.load(f)

    center = CITY_CENTERS[city_name]
    out = []
    for feat in gj["features"]:
        raw_name = feat["properties"].get("name", "")
        name = _clean_name(raw_name)
        if not name:
            continue
        lat, lon = _centroid(feat["geometry"])
        criteria = _generate_criteria(name, lat, lon, center)
        out.append({
            "name": name,
            "city": city_name,
            "lat": lat,
            "lon": lon,
            "geometry": feat["geometry"],
            "criteria": criteria,
        })
    return out


def all_districts():
    result = []
    for city in CITY_FILES:
        result.extend(_load_city(city))
    return result
