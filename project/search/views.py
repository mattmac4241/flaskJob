from functools import wraps

from flask import flash, redirect, render_template,request, session, url_for, Blueprint,abort
from project.models import Job,Company
from sqlalchemy_searchable import search

search_blueprint = Blueprint('search', __name__)

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

#search for jobs
def jobs_search(term):
    results = Job.query.search(term).all()
    return results

#search for companies
def companies_search(term):
    results = Company.query.search(term).all()
    return results

@search_blueprint.route('/search/jobs/', methods=['GET','POST'])
@login_required
def jobs():
    if request.method == 'POST':
        term = request.form['search']
        jobs = jobs_search(term)
        info = [(x,Company.query.get(x.company_id),str(x.date_added).split(' ')[0]) for x in jobs]
        return render_template('jobs_list.html',info=info)
    return render_template('jobs_list.html')

@search_blueprint.route('/search/companies/',methods=['GET','POST'])
@login_required
def companies():
    if request.method == 'POST':
        term = request.form['search']
        companies = companies_search(term)
        return render_template('companies_list.html',companies=companies)
    return render_template('companies_list.html')
