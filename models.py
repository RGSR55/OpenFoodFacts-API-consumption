from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    email= db.Column(db.String(50))
    password= db.Column(db.String(50))
    firstname= db.Column(db.String(50))
    lastname= db.Column(db.String(50))