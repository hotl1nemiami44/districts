import json
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False, index=True)

    # Координаты центра района
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # GeoJSON-полигон границ района (хранится как строка)
    geometry = db.Column(db.Text, nullable=True)

    # 10 критериев (оценки от 1 до 10)
    transport = db.Column(db.Float, default=0.0)
    education = db.Column(db.Float, default=0.0)
    healthcare = db.Column(db.Float, default=0.0)
    ecology = db.Column(db.Float, default=0.0)
    safety = db.Column(db.Float, default=0.0)
    shopping = db.Column(db.Float, default=0.0)
    leisure = db.Column(db.Float, default=0.0)
    amenities = db.Column(db.Float, default=0.0)
    noise = db.Column(db.Float, default=0.0)
    density = db.Column(db.Float, default=0.0)

    # Итоговый балл (1–100)
    total_score = db.Column(db.Float, default=0.0)

    def criteria_dict(self):
        return {
            "transport": round(self.transport, 1),
            "education": round(self.education, 1),
            "healthcare": round(self.healthcare, 1),
            "ecology": round(self.ecology, 1),
            "safety": round(self.safety, 1),
            "shopping": round(self.shopping, 1),
            "leisure": round(self.leisure, 1),
            "amenities": round(self.amenities, 1),
            "noise": round(self.noise, 1),
            "density": round(self.density, 1),
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "coordinates": [self.latitude, self.longitude],
            "criteria": self.criteria_dict(),
            "total_score": self.total_score,
        }

    def to_geojson_feature(self):
        geom = json.loads(self.geometry) if self.geometry else None
        return {
            "type": "Feature",
            "geometry": geom,
            "properties": {
                "id": self.id,
                "name": self.name,
                "city": self.city,
                "center": [self.latitude, self.longitude],
                "criteria": self.criteria_dict(),
                "total_score": self.total_score,
            },
        }
