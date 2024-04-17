from App.database import db

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    excersices = db.relationship('Excersice', backref=db.backref('routines', lazy=True))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('routines', lazy=True))

    def __init__(self, name, description, user_id):
        self.name = name
        self.description = description
        self.user_id = user_id