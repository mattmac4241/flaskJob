from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired,Length,optional

#form for those seeking a job
class CreateJobForm(Form):
    title = StringField(
        'Title',
        validators=[DataRequired(),Length(min=1,max=50)]
    )
    description = StringField(
        'Description',
        validators=[DataRequired(),Length(min=1,max=300)]
    )
    salary = IntegerField(
        'Salary',
        validators=[]
    )
    zip_code = StringField(
        'Zip Code',
        validators=[Length(min=5,max=5)])

    job_type = SelectField(
                'Job Type',
                choices=[(1, 'Full-Time'),
                         (2, 'Part-Time'),
                         (3, 'Contract'),
                         (4, 'Internship')],
                coerce=int,
                validators=[optional()])
