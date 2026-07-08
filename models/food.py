from database import db

class Food(db.Model):
    __tablename__ = 'food'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_allowed = db.Column(db.Boolean)