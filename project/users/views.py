from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from .forms import RegisterForm, LoginForm
from project import db, bcrypt,app
from project.models import User
from werkzeug import secure_filename
import os

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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def file_upload(name,file):
    path = app.config['UPLOAD_FOLDER']
    file_path = os.path.join("%s/%s" % (path,name))
    if not os.path.exists(file_path): #check if folder exists, if it doesn't creat it
        os.makedirs(file_path)
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "%s/%s" % (name,"profile_picture.jpg")))
    return "%s/%s" % (name,filename)

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
            image = form.image
            if image != None:
                file = request.files['image']
                p = file_upload(form.email.data,file)
                pa = "/static/files/users/%s" % p
                new_user = User(
                        name=form.first_name.data + ' ' + form.last_name.data,
                        email=form.email.data,
                        password=bcrypt.generate_password_hash(form.password.data),
                        profile_picture = pa
                )
            elif image == None:
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
    print "PICTURE " + user.profile_picture
    return render_template('user.html',user=user)
