from flask_wtf import Form
from wtforms import StringField,PasswordField,SelectField
from wtforms.validators import DataRequired,Length,EqualTo,Email

#form for those seeking a job
class RegisterForm(Form):
    first_name = StringField(
        'First Name',
        validators=[DataRequired(),Length(min=6,max=50)]
    )
    last_name = StringField(
        'Last Name',
        validators=[DataRequired(),Length(min=6,max=50)]
    )
    email = StringField(
        'Email',
        validators=[DataRequired(),Email(),Length(min=6,max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )

class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )
