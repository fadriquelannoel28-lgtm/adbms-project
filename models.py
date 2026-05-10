from flask_login import UserMixin
from extensions import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), default='Unknown') 
    phone = db.Column(db.String(20), default='Not Set')
    email = db.Column(db.String(100), unique=True, nullable=False)
    birthdate = db.Column(db.Date, default=None)
    profile_pic = db.Column(db.String(200), default='default-image.jpg')
    gov_id_pic = db.Column(db.String(200), nullable=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default='staff')
    verify = db.Column(db.Boolean, default=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return f'<User {self.username}>'

class MedInventory(db.Model):
    __tablename__ = "med_inventory"
    id = db.Column(db.Integer, primary_key=True)
    img_med = db.Column(db.String(200), default='images/thumbnail-med.jpg')
    medicine_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    dosage = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    per_price = db.Column(db.Float, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
