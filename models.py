from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), default='Unknown')
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), default='Unknown') 
    phone = db.Column(db.String(20), default='Not Set')
    email = db.Column(db.String(100), unique=True, default='Not Set')
    birthdate = db.Column(db.Date, default=None)
    profile_pic = db.Column(db.String(200), default='default-image.jpg')
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)