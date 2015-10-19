from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired,Length,EqualTo,Email

#form for those seeking a job
class CreateCompanyForm(Form):
    name = StringField(
        'Company Name',
        validators=[DataRequired(),Length(min=1,max=100)]
    )
    info = StringField(
        'Company Description',
        validators=[Length(min=1,max=200)]
    )
    website = StringField(
        'Website',
        validators=[Length(min=0,max=40)]
    )
