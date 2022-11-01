from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_number = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(4))
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(11))
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    resident = db.relationship('Resident', backref='user', lazy=True)
    visitor = db.relationship('Visitor', backref='user', lazy=True)

    def __init__(self, admin_number, title, name, surname, gender, email, password):
        self.admin_number = admin_number
        self.title = title
        self.first_name = name
        self.surname = surname
        self.gender = gender
        self.email = email
        self.password = password

    def __repr__(self):
        return f'User(first name: {self.first_name}, surname: {self.surname})'


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(4))
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(11))
    house_number = db.Column(db.Integer, nullable=False)
    car_reg = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)
    password = db.Column(db.String(10), nullable=False)
    profile_image = db.Column(db.String(225), unique=True)
    register = db.relationship('Register', backref='resident', lazy=True)

    def __init__(self, admin, id_number, title, name, surname, gender, house_number, car_reg, email, phone, password, profile_image):
        self.admin = admin
        self.title = title
        self.id_number = id_number
        self.first_name = name
        self.surname = surname
        self.gender = gender
        self.house_number = house_number
        self.car_reg = car_reg
        self.email = email
        self.phone = phone
        self.password = password
        self.profile_image = profile_image

    def __repr__(self):
        return f'Resident(first name: {self.first_name}, surname: {self.surname}, house: {self.house_number})'


class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(4))
    first_name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(11))
    car_reg = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(225), nullable=False)
    phone = db.Column(db.String(14), unique=True, nullable=False)
    profile_image = db.Column(db.String(225), unique=True)
    register = db.relationship('Register', backref='visitor', lazy=True)

    def __init__(self, admin, id_number, title, name, surname, gender, address, car_reg, email, phone, profile_image):
        self.admin = admin
        self.title = title
        self.id_number = id_number
        self.first_name = name
        self.surname = surname
        self.gender = gender
        self.address = address
        self.car_reg = car_reg
        self.email = email
        self.phone = phone
        self.profile_image = profile_image

    def __repr__(self):
        return f'Visitor(first name: {self.first_name}, surname: {self.surname}, address: {self.address})'


class Register(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.datetime.now)
    time_out = db.Column(db.DateTime)

    def __init__(self, visitor_id, resident_id):
        self.visitor_id = visitor_id
        self.resident_id = resident_id
