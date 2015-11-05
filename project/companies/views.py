from functools import wraps
from flask import flash, redirect, render_template,request, session, url_for, Blueprint

from .forms import CreateCompanyForm
from project import db, bcrypt,app
from project.models import Company,User,Job

import os

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

def file_upload(name,file,company_name):
    path = app.config['UPLOAD_FOLDER']
    file_path = os.path.join("%s/%s" % (path,name))
    if not os.path.exists(file_path): #check if folder exists, if it doesn't creat it
        os.makedirs(file_path)
    filename = "%s_profile_picture.jpg" % (company_name.replace(' ','_'))
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], "%s/%s" % (name,filename)))
    return "%s/%s" % (name,filename)


@companies_blueprint.route('/create_company/',methods=['GET','POST'])
@login_required
def create_company():
    error = None
    user = User.query.get(session['user_id'])
    form = CreateCompanyForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            print "HERE"
            image = form.image
            if image != None:
                file = request.files['image']
                p = file_upload(user.email,file,form.name.data)
                pa = "/static/files/users/%s" % p
                print pa
                new_company = Company(
                    name = form.name.data,
                    info = form.info.data,
                    website = form.website.data,
                    user_id = session['user_id'],
                    profile_picture = pa
                )
            else:
                new_company = Company(
                    name = form.name.data,
                    info = form.info.data,
                    website = form.website.data,
                    user_id = session['user_id']
                )
            try:
                print "HERE"
                user.companies.append(new_company)
                db.session.add(new_company)
                db.session.commit()
                flash("Thanks for registering your company")

            except IntegrityError:
                pass

            return redirect(url_for('companies.company_profile',company_id=new_company.id))
    return render_template('create_company.html',form=form)

@companies_blueprint.route('/company/<int:company_id>/')
@login_required
def company_profile(company_id):
    company = Company.query.get(company_id)
    return render_template('company.html',company=company)

@companies_blueprint.route('/company/<int:company_id>/jobs/')
@login_required
def company_jobs(company_id):
    company = Company.query.get(company_id)
    return render_template('company_jobs_list.html',company=company)

@companies_blueprint.route('/company/<int:company_id>/delete/')
@login_required
def delete_company(company_id):
    company = Company.query.get(company_id)
    if session['user_id'] == company.user_id:
        for job in company.jobs_posted:
            Job.query.filter_by(id=job.id).delete()
        Company.query.filter_by(id=company_id).delete()
        db.session.commit()
        flash('The company was deleted')
        return redirect(url_for('users.user_profile',user_id=session['user_id']))
    else:
        flash("You do not have permission for that")
        return redirect(url_for('companies.company_profile',company_id=company_id))
