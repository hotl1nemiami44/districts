from flask_sqlalchemy import SQLAlchemy

# Создаем объект базы данных (пока без привязки к приложению)
db = SQLAlchemy()


class District(db.Model):
    __tablename__ = 'districts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)

    # Координаты центра района (нужны фронтендеру для карты)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Наши 10 критериев (оценки от 1 до 10)
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

    # Итоговый балл (от 1 до 100)
    total_score = db.Column(db.Float, default=0.0)

    # Метод для превращения объекта в словарь (чтобы легко отдавать в JSON)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "coordinates": [self.latitude, self.longitude],
            "criteria": {
                "transport": self.transport,
                "education": self.education,
                "healthcare": self.healthcare,
                "ecology": self.ecology,
                "safety": self.safety,
                "shopping": self.shopping,
                "leisure": self.leisure,
                "amenities": self.amenities,
                "noise": self.noise,
                "density": self.density
            },
            "total_score": self.total_score
        }