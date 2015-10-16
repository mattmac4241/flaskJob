from functools import wraps
from flask import flash, redirect, render_template, \
    request, session, url_for, Blueprint
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

#routes
@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            #check to make sure this has no issues
            user = User.query.filter_by(email=request.form['email']).first()
            if user is not None and bcrypt.check_password_hash(
                    user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash("Welcome!")
                return render_template('test.html')
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

@users_blueprint.route('/register',methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(
                Name=form.first_name.data + ' ' + form.last_name.data,
                email=form.email.data,
                role = form.role.data,
                password=bcrypt.generate_password_hash(form.password.data)
            )
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Thanks for registering")
                return redirect(url_for('users.login'))
            except IntegrityError:
                error = "That username and/or email alread exists."
                return render_template('register.html',form=form,error=error)
    return render_template('register.html',form=form)
