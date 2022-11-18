from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
from enums import Choice

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_number = db.Column(db.Integer, unique=True)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    category = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(4))
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(11))
    address = db.Column(db.String(225), nullable=False)
    car_reg = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_image = db.Column(db.String(14), unique=True)
    qrcode_image = db.Column(db.String(14), unique=True)
    qrcode_word = db.Column(db.String(10), unique=True)
    register = db.relationship('Register', backref='user', lazy=True)

    def __repr__(self):
        return f'User(first name: {self.first_name}, surname: {self.surname})'

    def is_admin(self) -> bool:
        if self.category == Choice.ADMIN.value:
            return True
        else:
            return False


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    def __init__(self, user_id, time_in):
        self.user_id = user_id
        self.time_in = time_in

    def is_in(self):
        if self.time_in and not self.time_out:
            return True
        else:
            return False


