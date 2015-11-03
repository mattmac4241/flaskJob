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
    print Job.query.all()
    print term
    results = Job.query.search(term).all()
    return results

#search for companies
def companies_search(term):
    query = session.query(Comapny)
    query = search(query, term)
    return query

@search_blueprint.route('/search/jobs/', methods=['GET','POST'])
@login_required
def jobs():
    if request.method == 'POST':
        term = request.form['search']
        results = jobs_search(term)
        print "THESE ARE RESULTS %s" % results
        return render_template('jobs_list.html',results=results)
    return render_template('jobs_list.html')
