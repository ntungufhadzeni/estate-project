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

from models import User, Resident, Visitor

titles = [('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms'), ('miss', 'Miss'), ('dr', 'Dr'), ('prof', 'Prof')]
genders = [('male', 'Male'), ('female', 'Female'), ('non-binary', 'Non-Binary')]


def validate_phone(form, field):
    if len(field.data) > 10:
        raise ValidationError('Invalid phone number.')


def login_check(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if user is None:
        raise ValidationError('Username or password is incorrect')
    elif not check_password_hash(user.password, form.password.data):
        raise ValidationError('Username or password is incorrect')


def admin_number_validator(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if not user.admin_number == form.admin_number.data:
        raise ValidationError('Admin number is incorrect')


def unique_admin_validator(form, field):
    user = User.query.filter_by(admin_number=form.admin_number.data).first()
    if user:
        raise ValidationError('This admin number is already in use. Please try another one.')


def unique_email_validator(form, field):
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        raise ValidationError('This email is already in use. Please try another one.')


def unique_validator_resident(form, field):
    resident = Resident.query.filter_by(id_number=form.id_number.data).first()
    if resident:
        raise ValidationError('This ID number is already in use. Please try another one.')


def unique_validator_visitor(form, field):
    visitor = Visitor.query.filter_by(id_number=form.id_number.data).first()
    if visitor:
        raise ValidationError('This ID number is already in use. Please try another one.')


class LoginForm(FlaskForm):
    admin_number = IntegerField(
        'Admin Number',
        [
            DataRequired(message="This field is required."),
            admin_number_validator
        ]
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        [
            DataRequired(message="Please enter a password."),
            login_check
        ]
    )
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    admin_number = IntegerField(
        'Admin Number',
        [
            DataRequired(message="This field is required."),
            unique_admin_validator
        ]
    )
    title = SelectField(
        'Title',
        choices=titles,
        validators=[DataRequired(message="This field is required.")]
    )
    first_name = StringField(
        'First Name',
        [
            DataRequired(message="This field is required.")
        ]
    )
    surname = StringField(
        'Surname',
        [
            DataRequired(message="This field is required.")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=genders,
        validators=[DataRequired(message="This field is required.")]
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired(),
            unique_email_validator
        ]
    )
    password = PasswordField(
        'Password',
        [
            InputRequired(),
            EqualTo('confirmPassword', message='Passwords must match')
        ]
    )
    confirmPassword = PasswordField('Repeat Password')
    submit = SubmitField('Submit')


class ResidentForm(FlaskForm):
    id_number = IntegerField(
        'ID/Passport Number',
        [
            DataRequired(message="This field is required."),
            unique_validator_resident
        ]
    )
    title = SelectField(
        'Title',
        choices=titles,
        validators=[DataRequired(message="This field is required.")]
    )
    first_name = StringField(
        'First Name',
        [
            DataRequired(message="This field is required.")
        ]
    )
    surname = StringField(
        'Surname',
        [
            DataRequired(message="This field is required.")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=genders,
        validators=[DataRequired(message="This field is required.")]
    )
    house_number = IntegerField(
        'House No.',
        [
            DataRequired(message="This field is required.")
        ]
    )
    car_reg = StringField(
        'Car Registration',
        [
            DataRequired(message="This field is required.")
        ]
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired(message="This field is required.")
        ]
    )
    phone = StringField(
        'Cellphone',
        [
            DataRequired(message="This field is required."),
            validate_phone
        ]
    )
    password = StringField(
        'Password',
        [
            DataRequired(message="This field is required."),
        ]
    )
    upload = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Add Resident')


class VisitorForm(FlaskForm):
    id_number = IntegerField(
        'ID/Passport Number',
        [
            DataRequired(message="This field is required."),
            unique_validator_visitor
        ]
    )
    title = SelectField(
        'Title',
        choices=titles,
        validators=[DataRequired(message="This field is required.")]
    )
    first_name = StringField(
        'First Name',
        [
            DataRequired(message="This field is required.")
        ]
    )
    surname = StringField(
        'Surname',
        [
            DataRequired(message="This field is required.")
        ]
    )
    gender = SelectField(
        'Gender',
        choices=genders,
        validators=[DataRequired(message="This field is required.")]
    )
    address = StringField(
        'Address',
        [
            DataRequired(message="This field is required.")
        ]
    )
    car_reg = StringField(
        'Car Registration',
        [
            DataRequired(message="This field is required.")
        ]
    )
    email = StringField(
        'Email',
        [
            Email(message='Not a valid email address.'),
            DataRequired(message="This field is required.")
        ]
    )
    phone = StringField(
        'Cellphone',
        [
            DataRequired(message="This field is required."),
            validate_phone
        ]
    )
    upload = FileField('Profile Picture', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Add Visitor')
