from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import RegisterForm, LoginForm
from project import db, bcrypt
from project.models import User

users_blueprint = Blueprint('users', __name__)

#Helper functions
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

@users_blueprint.route('/')
def index():
    if 'logged_in' in session:
        name = session['name']
        return render_template('index.html',name=name)
    return render_template('index.html')

#routes
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            #check to make sure this has no issues
            user = User.query.filter_by(email=request.form['email']).first()
            if user is not None and bcrypt.check_password_hash(user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash("Welcome!")
                flash("Succesfful Logged in")
                return redirect(url_for('users.index')) #when profiles are designed change to profiles
            else:
                error = 'Invalid username or password.'
    return render_template('login.html',form=form,error=error)

@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('role',None)
    session.pop('name',None)
    flash("Goodbye!")
    return redirect(url_for('users.login'))

@users_blueprint.route('/register/',methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                name=form.first_name.data + ' ' + form.last_name.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks for registering")
                return redirect(url_for('users.index'))
            except IntegrityError:
                error = "That username and/or email alread exists."
                return render_template('register.html',form=form,error=error)
    return render_template('register.html',form=form)


@users_blueprint.route('/user/<int:user_id>/')
@login_required
def user_profile(user_id):
    user = User.query.get(user_id)
    return render_template('user.html',user=user)
