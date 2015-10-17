from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint
from sqlalchemy.exc import IntegrityError

from .forms import CreateCompanyForm
from project import db, bcrypt
from project.models import Company

users_blueprint = Blueprint('companies', __name__)

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

@users_blueprint.route('/create_company/',methods=['GET','POST'])
def create_company():
    error = None
    form = CreateCompanyForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_company = Comapny(
                name = form.name.data,
                info = form.info.data,
                field = form.field.data,
                website = form.website.data
            )
            try:
                db.session.add(new_company)
                db.session.commit()
                flash("Thanks for registering your company")
                return redirect(url_for('companies.profile'))
    return render_template('create_company.html',form=form)
