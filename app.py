import datetime
import os

from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from sqlalchemy import or_, desc, func
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import qrcode
import string
import random

from forms import LoginForm, AdminForm, ResidentForm, VisitorForm
from models import db, User, Register
from send_email import send_email

basedir = os.path.abspath(os.path.dirname(__file__))
qrcode_path = os.path.join(basedir, 'static', 'qrcodes')
photos_path = os.path.join(basedir, 'static', 'photos')

if not os.path.exists(photos_path):
    os.makedirs(photos_path)

if not os.path.exists(qrcode_path):
    os.makedirs(qrcode_path)


def unique_photo_filename():
    word = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))
    user = User.query.filter(User.profile_image.like(word)).first()
    if user:
        unique_photo_filename()
    else:
        return word


def unique_qrcode_filename():
    word = ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(10))
    user = User.query.filter_by(qrcode_word=word).first()
    if user:
        unique_qrcode_filename()
    else:
        return word


app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = os.urandom(15)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app=app, db=db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            remember = True if form.remember_me.data else False
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=remember)
                if user.is_admin():
                    return redirect(url_for('view_admin_profile', user_id=user.id))
                else:
                    return redirect(url_for('view_profile', user_id=user.id))
    return render_template('login.html', form=form)


@app.route('/admin-signup', methods=['POST', 'GET'])
def admin_signup():
    form = AdminForm()
    if form.validate_on_submit():
        admin_number = form.admin_number.data
        id_number = form.id_number.data
        title = form.title.data
        first_name = form.first_name.data
        surname = form.surname.data
        gender = form.gender.data
        email = form.email.data
        address = form.address.data
        car_reg = form.car_reg.data
        phone = form.phone.data
        category = 0
        password = generate_password_hash(form.password.data, method='sha256')

        f = form.upload.data
        word = unique_photo_filename()
        filename = f'{word}{secure_filename(f.filename)[-4:]}'
        f.save(os.path.join(basedir, 'static', 'photos', filename))
        new_user = User(admin_number=admin_number, id_number=id_number, category=category, title=title,
                        first_name=first_name, surname=surname, gender=gender, email=email, address=address,
                        car_reg=car_reg, phone=phone, password=password, profile_image=filename)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('admin_signup'))
    return render_template('admin_signup.html', form=form)


@app.route('/')
def home():
    return render_template('index.html')


@login_required
@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@login_required
@app.route('/residents-signup', methods=['GET', 'POST'])
def residents_signup():
    form = ResidentForm()
    if form.validate_on_submit():
        id_number = form.id_number.data
        title = form.title.data
        first_name = form.first_name.data
        surname = form.surname.data
        gender = form.gender.data
        email = form.email.data
        address = form.address.data
        car_reg = form.car_reg.data
        phone = form.phone.data
        category = 1
        password = generate_password_hash(form.password.data, method='sha256')

        f = form.upload.data
        word = unique_photo_filename()
        filename = f'{word}{secure_filename(f.filename)[-4:]}'
        f.save(os.path.join(basedir, 'static', 'photos', filename))
        new_user = User(id_number=id_number, category=category, title=title,
                        first_name=first_name, surname=surname, gender=gender, email=email, address=address,
                        car_reg=car_reg, phone=phone, password=password, profile_image=filename)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('residents_signup'))
    return render_template('resident_signup.html', form=form)


@login_required
@app.route('/visitors-signup', methods=['GET', 'POST'])
def visitors_signup():
    form = VisitorForm()
    if form.validate_on_submit():
        id_number = form.id_number.data
        title = form.title.data
        first_name = form.first_name.data
        surname = form.surname.data
        gender = form.gender.data
        email = form.email.data
        address = form.address.data
        car_reg = form.car_reg.data
        phone = form.phone.data
        category = 2
        password = generate_password_hash(form.password.data, method='sha256')

        f = form.upload.data
        word = unique_photo_filename()
        filename = f'{word}{secure_filename(f.filename)[-4:]}'
        f.save(os.path.join(basedir, 'static', 'photos', filename))
        new_user = User(id_number=id_number, category=category, title=title,
                        first_name=first_name, surname=surname, gender=gender, email=email, address=address,
                        car_reg=car_reg, phone=phone, password=password, profile_image=filename)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('visitors_signup'))
    return render_template('visitor_signup.html', form=form)


@login_required
@app.route('/profile/<int:user_id>')
def view_profile(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)
        return render_template('resident_visitor.html', user=user)


@login_required
@app.route('/admin-profile/<int:user_id>')
def view_admin_profile(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)
        return render_template('admin.html', user=user)


@app.route('/view-user-qrcode/<int:user_id>')
def view_user_qrcode(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)
        if user.is_admin():
            return render_template('qrcode_admin.html', user=user)
        else:
            return render_template('qrcode_resident_visitor.html', user=user)


@app.route('/generate-user-qr-code/<int:user_id>')
def generate_user_qrcode(user_id):
    if current_user.is_authenticated:
        user = User.query.get_or_404(user_id)
        ip_address = request.remote_addr
        word = unique_qrcode_filename()
        data = f'http://{ip_address}:8000/verify/{word}'
        img = qrcode.make(data)
        filename = word + '.png'
        user.qrcode_image = filename
        user.qrcode_word = word
        db.session.commit()
        img.save(f'./static/qrcodes/{filename}')
        file_path = os.path.join(basedir, 'static', 'qrcodes', filename)
        # send_email(file_path, user.first_name, user.email)
        if user.is_admin():
            return render_template('qrcode_admin.html', user=user)
        else:
            return render_template('qrcode_resident_visitor.html', user=user)


@app.route('/verify/<string:qrcode_word>')
def register_add_user(qrcode_word):
    user = User.query.filter_by(qrcode_word=qrcode_word).first()
    if not user:
        return render_template('unknown.html')

    try:
        user_to_register = Register.query.filter_by(user_id=user.id).order_by(desc(Register.id)).first()
    except IndexError:
        user_to_register = Register.query.filter_by(user_id=user.id)

    if not user_to_register or not user_to_register.is_in():
        now = datetime.datetime.now()
        user_to_register = Register(user.id, now)

        db.session.add(user_to_register)
        db.session.commit()
        check = "Check-In"
        tm = f"Time: {now.strftime('%H:%M')}"
        return render_template('success.html', user=user, check=check, tm=tm)
    elif user_to_register.is_in():
        now = datetime.datetime.now()
        user_to_register.time_out = now
        db.session.commit()
        check = "Check-Out"
        tm = f"Time: {now.strftime('%H:%M')}"
        return render_template('success.html', user=user, check=check, tm=tm)
    else:
        return render_template('unknown.html')


@login_required
@app.route('/register', methods=['GET', 'POST'])
def view_register():
    if current_user.is_authenticated:
        user = current_user
        return render_template('register.html', user=user)


@app.route("/ajax-live-search-register", methods=["POST", "GET"])
def ajax_live_search_register():
    if request.method == 'POST':
        try:
            search_word = request.form['query']
        except KeyError:
            search_word = ''
        if search_word == '':
            register = Register.query.order_by(desc(Register.id)).limit(10)
        else:
            search = "%{}%".format(search_word)
            register = Register.query.filter(or_(Register.user.has(User.first_name.like(search)),
                                                 Register.user.has(User.surname.like(search)))).all()
        return jsonify({'htmlresponse': render_template('response_register.html', register=register)})


@login_required
@app.route('/visitors', methods=['GET', 'POST'])
def view_visitors():
    if current_user.is_authenticated:
        user = current_user
        return render_template('visitors.html', user=user)


@app.route("/ajax-live-search-visitors", methods=["POST", "GET"])
def ajax_live_search_Visitors():
    if request.method == 'POST':
        try:
            search_word = request.form['query']
        except KeyError:
            search_word = ''
        if search_word == '':
            visitors = User.query.filter_by(category=2).order_by(desc(User.id)).limit(10)
        else:
            search = "%{}%".format(search_word)
            visitors = User.query.filter_by(category=2).filter(or_(User.first_name.like(search),
                                                                   User.surname.like(search),
                                                                   User.email.like(search))).all()
        return jsonify({'htmlresponse': render_template('response_visitors.html', visitors=visitors)})


@login_required
@app.route('/residents', methods=['GET', 'POST'])
def view_residents():
    if current_user.is_authenticated:
        user = current_user
        return render_template('residents.html', user=user)


@app.route("/ajax-live-search-residents", methods=["POST", "GET"])
def ajax_live_search_residents():
    if request.method == 'POST':
        try:
            search_word = request.form['query']
        except KeyError:
            search_word = ''
        if search_word == '':
            residents = User.query.filter_by(category=1).order_by(desc(User.id)).limit(10)
        else:
            search = "%{}%".format(search_word)
            residents = User.query.filter_by(category=1).filter(or_(User.first_name.like(search),
                                                                    User.surname.like(search),
                                                                    User.email.like(search))).all()

        return jsonify({'htmlresponse': render_template('response_residents.html', residents=residents)})


@login_required
@app.route('/delete-resident/<int:resident_id>')
def delete_resident(resident_id):
    if current_user.is_authenticated:
        resident_to_delete = User.query.get_or_404(resident_id)
        try:
            db.session.delete(resident_to_delete)
            db.session.commit()
            flash('The user has been deleted!')
            return redirect(url_for('view_residents'))
        except:
            flash('There was an issue deleting the user!')
            return redirect(url_for('view_residents'))


@app.route('/delete-visitor/<int:visitor_id>')
def delete_visitor(visitor_id):
    if current_user.is_authenticated:
        visitor_to_delete = User.query.get_or_404(visitor_id)
        try:
            db.session.delete(visitor_to_delete)
            db.session.commit()
            flash('The visitor has been deleted!')
            return redirect(url_for('view_visitors'))
        except:
            flash('There was an issue deleting the visitor!')
            return redirect(url_for('view_visitors'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
