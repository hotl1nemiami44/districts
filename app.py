from flask import Flask, jsonify, render_template
from database.config import Config
from database.models import db, District
from core.parser import fetch_and_save_mock_data
import logging


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Добавляем принудительный вывод в консоль
        print("Проверка базы данных...")
        fetch_and_save_mock_data(app)

    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


# НОВЫЙ ДИАГНОСТИЧЕСКИЙ РОУТ
@app.route('/api/test-all')
def test_all():
    """Показывает все записи в базе, чтобы проверить, не пуста ли она"""
    all_districts = District.query.all()
    print(f"Запрос к БД: найдено {len(all_districts)} районов")
    return jsonify([d.to_dict() for d in all_districts])


@app.route('/api/districts/<city>', methods=['GET'])
def get_districts(city):
    # Убедись, что город в базе и в запросе совпадает по регистру
    search_city = city.strip().capitalize()
    districts = District.query.filter_by(city=search_city).all()

    if not districts:
        return jsonify(
            {"message": f"В городе {search_city} районов не найдено", "db_count": District.query.count()}), 404

    return jsonify([d.to_dict() for d in districts])


if __name__ == '__main__':
    app.run(debug=True, port=5000)