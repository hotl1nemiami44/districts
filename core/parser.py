import random
from database.models import db, District
from core.analyzer import calculate_rating


def fetch_and_save_mock_data(app):
    """
    Генерирует тестовые районы для Москвы, считает их баллы и сохраняет в БД.
    """
    districts_data = [
        {"name": "Тверской", "city": "Moscow", "lat": 55.76, "lon": 37.61},
        {"name": "Хамовники", "city": "Moscow", "lat": 55.72, "lon": 37.57},
        {"name": "Бирюлево", "city": "Moscow", "lat": 55.59, "lon": 37.65}
    ]

    with app.app_context():
        # Если в базе уже есть районы, не добавляем их снова
        if District.query.first():
            return

        for d_info in districts_data:
            # 1. Парсер "собирает" данные (здесь генерируем случайные от 1 до 10)
            criteria = {
                "transport": random.uniform(3, 10),
                "education": random.uniform(3, 10),
                "healthcare": random.uniform(3, 10),
                "ecology": random.uniform(1, 10),
                "safety": random.uniform(2, 10),
                "shopping": random.uniform(5, 10),
                "leisure": random.uniform(4, 10),
                "ameni  ties": random.uniform(3, 10),
                "noise": random.uniform(1, 10),  # 10 - тихо, 1 - шумно
                "density": random.uniform(1, 10)
            }

            # 2. Отдаем данные в функцию Дата Сайентиста для получения общего балла
            total = calculate_rating(criteria)

            # 3. Сохраняем всё в базу данных
            new_district = District(
                name=d_info["name"],
                city=d_info["city"],
                latitude=d_info["lat"],
                longitude=d_info["lon"],
                **criteria,  # Распаковываем словарь критериев
                total_score=total
            )
            db.session.add(new_district)

        db.session.commit()
        print("Тестовые данные успешно добавлены в БД!")