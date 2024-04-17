'''
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
'''
from App.database import db

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    equipment = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('excersices', lazy=True))

    def __init__(self, name, description, duration, equipment, user_id):
        self.name = name
        self.duration = duration
        self.equipment = equipment 
        self.description = description
        self.user_id = user_id