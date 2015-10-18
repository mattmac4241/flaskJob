from functools import wraps

from flask import flash, redirect, render_template,request, session, url_for, Blueprint,abort
from sqlalchemy.exc import IntegrityError

from .forms import CreateJobForm
from project import db
from project.models import Job,Company

jobs_blueprint = Blueprint('jobs', __name__)

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

@jobs_blueprint.route('/company/<int:company_id>/create_job/',methods=['GET','POST'])
@login_required
def create_job(company_id):
    print "here"
    error = None
    form = CreateJobForm(request.form)
    user = session['user_id']
    company = Company.query.get(company_id)
    if company.user_id != user:
        abort(403)
    elif request.method == 'POST':
        if form.validate_on_submit():
            new_job = Job(
                title = form.title.data,
                description = form.description.data,
                salary = form.salary.data,
                zip_code = form.zip_code.data,
                job_type = form.job_type.data,
                company_id = company.id
            )
            db.session.add(new_job)
            db.session.commit()
            flash("Thanks for posting a job")
            return redirect(url_for('jobs.jobs_profile',company_id=company.id,jobs_id=new_job.id))
    return render_template('create_job.html',form=form)

@jobs_blueprint.route('/company/<int:company_id>/jobs/<int:jobs_id>')
@login_required
def jobs_profile(jobs_id,company_id):
    job = Job.query.get(jobs_id)
    return render_template('job.html',job=job)

@jobs_blueprint.route('/apply_to/<int:jobs_id>')
@login_required
def apply_to_job(jobs_id):
    job = Jobs.query.get(jobs_id)
    user = User.query.get(session['user_id'])
    user.applied_to.append(job)
    job.applied_to.append(user)
    db.session.commit()
    flash('You successfully applied to the job. Good Luck!')
    return redirect(url_for('jobs.profile',jobs_id=jobs_id,company_id=jobs.company_id))
