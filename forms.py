from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.security import check_password_hash
from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    PasswordField,
    SelectField,
    BooleanField
)
from wtforms import ValidationError
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    InputRequired
)

from models import User
from enums import Choice


titles = [(Choice.DEFAULT.value, Choice.DEFAULT.value), ('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms'), ('miss', 'Miss'), ('dr', 'Dr'),
          ('prof', 'Prof')]
genders = [(Choice.DEFAULT.value, Choice.DEFAULT.value), ('male', 'Male'), ('female', 'Female'), ('non-binary', 'Non-Binary'),
           ('other', 'Other')]


def validate_phone(form, field):
    if len(field.data) > 10:
        raise ValidationError('Invalid phone number.')


def login_check(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if user is None:
        raise ValidationError('Username or password is incorrect')
    elif not check_password_hash(user.password, form.password.data):
        raise ValidationError('Username or password is incorrect')


def unique_admin_validator(form, field):
    user = User.query.filter_by(admin_number=form.admin_number.data).first()
    if user:
        raise ValidationError('This admin number is already in use. Please try another one.')


def unique_email_validator(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        raise ValidationError('This email is already in use. Please try another one.')


def unique_id_validator(form, field):
    user = User.query.filter_by(id_number=form.id_number.data).first()
    if user:
        raise ValidationError('This ID number is already in use. Please try another one.')


def unique_phone_validator(form, field):
    user = User.query.filter_by(phone=form.phone.data).first()
    if user:
        raise ValidationError('This cellphone number is already in use. Please try another one.')


def gender_choose_validator(form, field):
    if form.gender.data == Choice.DEFAULT.value:
        raise ValidationError("Gender is required")


def title_choose_validator(form, field):
    if form.title.data == Choice.DEFAULT.value:
        raise ValidationError("Title is required")


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired(message="Please enter your email address")
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password"),
            login_check
        ]
    )
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class AdminForm(FlaskForm):
    admin_number = IntegerField(
        'Admin Number',
        [
            DataRequired(message="Admin is required"),
            unique_admin_validator
        ]
    )
    id_number = IntegerField(
        'ID/Passport Number',
        [
            DataRequired(message="ID/Passport is required"),
            unique_id_validator
        ]
    )
    title = SelectField(
        'Title',
        choices=titles,
        validators=[title_choose_validator]
    )
    first_name = StringField(
        'First Names',
        [
            DataRequired(message="First name is required")
        ]
    )
    surname = StringField(
        'Surname',
        [
            DataRequired(message="Surname is required")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=genders,
        validators=[gender_choose_validator]
    )
    address = StringField(
        'Home Address',
        [
            DataRequired(message="Address is required")
        ]
    )
    car_reg = StringField(
        'Car Registration'
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address'),
            DataRequired(message="Email is required"),
            unique_email_validator
        ]
    )
    phone = StringField(
        'Cellphone',
        [
            DataRequired(message="Cellphone number is required"),
            validate_phone,
            unique_phone_validator
        ]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired('Please enter a password'),
            EqualTo('confirmPassword', message='Passwords must match')
        ]
    )
    confirmPassword = PasswordField('Repeat Password')
    upload = FileField('Profile Picture', validators=[
        FileRequired(message="Please choose a file"),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Sign Up')


class ResidentForm(FlaskForm):
    id_number = IntegerField(
        'ID/Passport Number',
        [
            DataRequired(message="ID/Password is required"),
            unique_id_validator
        ]
    )
    title = SelectField(
        'Title',
        choices=titles,
        validators=[title_choose_validator]
    )
    first_name = StringField(
        'First Names',
        [
            DataRequired(message="First name is required")
        ]
    )
    surname = StringField(
        'Surname',
        [
            DataRequired(message="Surname is required")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=genders,
        validators=[gender_choose_validator]
    )
    address = StringField(
        'Home Address',
        [
            DataRequired(message="Address is required")
        ]
    )
    car_reg = StringField(
        'Car Registration'
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address'),
            DataRequired(message="Email is required"),
            unique_email_validator
        ]
    )
    phone = StringField(
        'Cellphone',
        [
            DataRequired(message="Cellphone number is required"),
            validate_phone,
            unique_phone_validator
        ]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired('Please enter a '
                          'password'),
            EqualTo('confirmPassword', message='Passwords must match')
        ]
    )
    confirmPassword = PasswordField('Repeat Password')
    upload = FileField('Profile Picture', validators=[
        FileRequired(message="Please choose a file"),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Sign Up')


class VisitorForm(FlaskForm):
    id_number = IntegerField(
        'ID/Passport Number',
        [
            DataRequired(message="ID/Passport is required"),
            unique_id_validator
        ]
    )
    title = SelectField(
        'Title',
        choices=titles,
        validators=[title_choose_validator]
    )
    first_name = StringField(
        'First Names',
        [
            DataRequired(message="First name is required")
        ]
    )
    surname = StringField(
        'Surname',
        [
            DataRequired(message="Surname is required")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=genders,
        validators=[gender_choose_validator]
    )
    address = StringField(
        'Home Address',
        [
            DataRequired(message="Address is required")
        ]
    )
    car_reg = StringField(
        'Car Registration'
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address'),
            DataRequired(message="Email is required"),
            unique_email_validator
        ]
    )
    phone = StringField(
        'Cellphone',
        [
            DataRequired(message="Cellphone is required"),
            validate_phone,
            unique_phone_validator
        ]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired(message="Please enter a password"),
            EqualTo('confirmPassword', message='Passwords must match')
        ]
    )
    confirmPassword = PasswordField('Repeat Password')
    upload = FileField('Profile Picture', validators=[
        FileRequired(message="Please choose a file"),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Sign Up')
