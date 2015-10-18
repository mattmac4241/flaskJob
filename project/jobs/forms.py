from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired,Length

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
        validators=[])

    job_type = StringField(
        'Job Type',
        validators=[Length(min=5,max=20)]
    )
