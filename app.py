import datetime
import os

from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from sqlalchemy import or_, desc
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from forms import LoginForm, SignupForm, ResidentForm, VisitorForm
from models import db, User, Resident, Visitor, Register

basedir = os.path.abspath(os.path.dirname(__file__))

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


@app.errorhandler(400)
def not_found(e):
    return render_template("400.html"), 400


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            remember = True if form.remember_me.data else False
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=remember)
                return redirect(url_for('home'))
    return render_template('login.html', form=form)


@app.route('/signup', methods=['POST', 'GET'])
def signup_post():
    form = SignupForm()
    if form.validate_on_submit():
        admin_number = form.admin_number.data
        title = form.title.data
        first_name = form.first_name.data
        surname = form.surname.data
        gender = form.gender.data
        email = form.email.data
        password = generate_password_hash(form.password.data, method='sha256')

        new_user = User(admin_number, title, first_name, surname, gender, email, password)
        db.session.add(new_user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('signup_post'))
    return render_template('signup.html', form=form)


@login_required
@app.route('/home')
def home():
    if current_user.is_authenticated:
        name = f'{current_user.first_name.capitalize()} {current_user.surname.capitalize()}'
        return render_template('index.html', name=name)
    else:
        return redirect(url_for('login'))


@login_required
@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@login_required
@app.route('/residents', methods=['GET', 'POST'])
def add_resident():
    if current_user.is_authenticated:
        user = current_user.id
        form = ResidentForm()
        if form.validate_on_submit():
            f = form.upload.data
            filename = f'{form.first_name.data}_{form.surname.data}_{form.house_number.data}{secure_filename(f.filename)[-4:]}'
            f.save(os.path.join(basedir, 'static', 'photos', filename))
            new_resident = Resident(user, form.id_number.data, form.title.data, form.first_name.data, form.surname.data,
                                    form.gender.data, form.house_number.data, form.car_reg.data, form.email.data,
                                    form.phone.data, form.password.data, filename)
            try:
                db.session.add(new_resident)
                db.session.commit()
                flash('Resident has been added successfully')
                return redirect(url_for('add_resident'))
            except:
                flash('There was an issue adding new resident')
                return render_template('residents.html', form=form)
        return render_template('residents.html', form=form)


@login_required
@app.route('/resident/<int:resident_id>')
def view_resident(resident_id):
    if current_user.is_authenticated:
        resident = Resident.query.get_or_404(resident_id)
        return render_template('resident.html', resident=resident)


@login_required
@app.route('/register', methods=['GET'])
def view_register():
    if current_user.is_authenticated:
        return render_template('register.html')


@login_required
@app.route('/visitor/<int:visitor_id>')
def view_visitor(visitor_id):
    if current_user.is_authenticated:
        visitor = Visitor.query.get_or_404(visitor_id)
        return render_template('visitor.html', visitor=visitor)


@login_required
@app.route('/delete/<int:resident_id>')
def delete_resident(resident_id):
    if current_user.is_authenticated:
        resident_to_delete = Resident.query.get_or_404(resident_id)
        try:
            db.session.delete(resident_to_delete)
            db.session.commit()
            flash('The user has been deleted!')
            return redirect(url_for('add_resident'))
        except:
            flash('There was an issue deleting the user!')
            return redirect(url_for('add_resident'))


@login_required
@app.route('/register-visitor/<int:resident_id>')
def register_resident(resident_id):
    form = VisitorForm()
    session['resident_id'] = resident_id
    return render_template('visitors.html', form=form)


@login_required
@app.route('/register/<int:resident_id>/<int:visitor_id>', methods=['GET', 'POST'])
def register_visitor(resident_id, visitor_id):
    if current_user.is_authenticated:
        register = Register(visitor_id, resident_id)
        try:
            db.session.add(register)
            db.session.commit()
            flash('Vistor has been added to register!')
            return render_template('register.html')
        except:
            flash('There was an issue registering the user!')
            return render_template('register.html')


@login_required
@app.route('/update-register/<int:register_id>', methods=['GET', 'POST'])
def update_register(register_id):
    if current_user.is_authenticated:
        register_to_update = Register.query.get_or_404(register_id)
        now = datetime.datetime.now()
        try:
            register_to_update.time_out = now
            db.session.commit()
            flash('Vistor has been checked out!')
            return render_template('register.html')
        except:
            flash('There was an issue checking out the visitor. please try again')
            return render_template('register.html')


@app.route("/ajaxlivesearch", methods=["POST", "GET"])
def ajaxlivesearch():
    if request.method == 'POST':
        try:
            search_word = request.form['query']
        except KeyError:
            search_word = ''
        if search_word == '':
            residents = Resident.query.order_by(desc(Resident.id)).limit(10)
        else:
            search = "%{}%".format(search_word)
            residents = Resident.query.filter(or_(Resident.first_name.like(search),
                                                  Resident.surname.like(search),
                                                  Resident.email.like(search))).all()
        return jsonify({'htmlresponse': render_template('response.html', residents=residents)})


@login_required
@app.route('/add-visitor', methods=['GET', 'POST'])
def add_visitor():
    if current_user.is_authenticated:
        user = current_user.id
        form = VisitorForm()
        if form.validate_on_submit():
            f = form.upload.data
            filename = f'{form.first_name.data}_{form.surname.data}_visitor_{secure_filename(f.filename)[-4:]}'
            f.save(os.path.join(basedir, 'static', 'photos', filename))
            new_visitor = Visitor(user, form.id_number.data, form.title.data, form.first_name.data, form.surname.data,
                                  form.gender.data, form.address.data, form.car_reg.data, form.email.data,
                                  form.phone.data, filename)
            try:
                db.session.add(new_visitor)
                db.session.commit()
                flash('Visitor has been added successfully')
                return redirect(url_for('add_visitor'))
            except:
                flash('There was an issue adding new visitor')
                return render_template('visitors.html', form=form)
        return render_template('visitors.html', form=form)


@app.route("/ajaxlivesearchVisitors", methods=["POST", "GET"])
def ajaxlivesearchVisitors():
    if request.method == 'POST':
        try:
            search_word = request.form['query']
            resident_id = session['resident_id']
        except KeyError:
            search_word = ''
            resident_id = 1
        if search_word == '':
            visitors = Visitor.query.order_by(desc(Visitor.id)).limit(10)
        else:
            search = "%{}%".format(search_word)
            visitors = Visitor.query.filter(or_(Visitor.first_name.like(search),
                                                Visitor.surname.like(search),
                                                Visitor.email.like(search))).all()
        return jsonify(
            {'htmlresponse': render_template('response_visitors.html', visitors=visitors, resident_id=resident_id)})


@app.route("/ajaxlivesearchRegister", methods=["POST", "GET"])
def ajaxlivesearchRegister():
    if request.method == 'POST':
        try:
            search_word = request.form['query']
        except KeyError:
            search_word = ''
        if search_word == '':
            register = Register.query.order_by(desc(Register.id)).limit(10)
        else:
            search = "%{}%".format(search_word)
            register = Register.query.filter(or_(Register.visitor.has(Visitor.first_name.like(search)),
                                                 Register.visitor.has(Visitor.surname.like(search)))).all()
        return jsonify({'htmlresponse': render_template('response_register.html', register=register)})


@app.route('/delete-visitor/<int:visitor_id>')
def delete_visitor(visitor_id):
    if current_user.is_authenticated:
        visitor_to_delete = Visitor.query.get_or_404(visitor_id)
        try:
            db.session.delete(visitor_to_delete)
            db.session.commit()
            flash('The visitor has been deleted!')
            return redirect(url_for('add_visitor'))
        except:
            flash('There was an issue deleting the visitor!')
            return redirect(url_for('add_visitor'))


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
