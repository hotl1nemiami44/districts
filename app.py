from flask import Flask, jsonify, render_template
from database.config import Config
from database.models import db, District
from core.parser import fetch_and_save_mock_data


CITY_LABELS = {
    "Moscow": "Москва",
    "Saint-Petersburg": "Санкт-Петербург",
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()
        fetch_and_save_mock_data(app)

    return app


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/cities', methods=['GET'])
def get_cities():
    rows = db.session.query(District.city).distinct().all()
    cities = [
        {"id": c[0], "label": CITY_LABELS.get(c[0], c[0])}
        for c in rows
    ]
    return jsonify(cities)


@app.route('/api/districts/<city>', methods=['GET'])
def get_districts(city):
    districts = District.query.filter_by(city=city).all()
    if not districts:
        return jsonify({"message": f"В городе {city} районов не найдено"}), 404

    features = [d.to_geojson_feature() for d in districts]
    return jsonify({
        "type": "FeatureCollection",
        "city": city,
        "features": features,
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
