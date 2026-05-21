import json
from database.models import db, District
from core.analyzer import calculate_rating
from core.mock_data import all_districts


def fetch_and_save_mock_data(app):
    """
    Загружает mock-данные районов (Москва, СПб) с GeoJSON-полигонами,
    считает рейтинг и сохраняет в БД.
    """
    with app.app_context():
        if District.query.first():
            return

        for d in all_districts():
            criteria = d["criteria"]
            total = calculate_rating(criteria)

            district = District(
                name=d["name"],
                city=d["city"],
                latitude=d["lat"],
                longitude=d["lon"],
                geometry=json.dumps(d["geometry"], ensure_ascii=False),
                total_score=total,
                **criteria,
            )
            db.session.add(district)

        db.session.commit()
        print(f"Тестовые данные загружены: {District.query.count()} районов")
