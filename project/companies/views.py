from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint

from .forms import CreateCompanyForm
from project import db, bcrypt
from project.models import Company

companies_blueprint = Blueprint('companies', __name__)

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

@companies_blueprint.route('/create_company/',methods=['GET','POST'])
@login_required
def create_company():
    error = None
    form = CreateCompanyForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_company = Company(
                name = form.name.data,
                info = form.info.data,
                website = form.website.data,
                user_id = session['user_id']
            )
            db.session.add(new_company)
            db.session.commit()
            flash("Thanks for registering your company")
            return redirect(url_for('companies.company_profile',company_id=new_company.id))
    return render_template('create_company.html',form=form)

@companies_blueprint.route('/company/<int:company_id>')
@login_required
def company_profile(company_id):
    company = Company.query.get(company_id)
    return render_template('company.html',company=company)
