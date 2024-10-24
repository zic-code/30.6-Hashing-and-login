from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, Email

class RegisterForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(max =20)])
    password = PasswordField('Password', validators= [InputRequired()])
    email = EmailField('Email', validators = [InputRequired(),Email(),Length(max=50)])
    first_name = StringField('First_name',validators = [InputRequired(), Length(max=30)])
    last_name= StringField('Last_name',validators = [InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    username = StringField('Username',validators =[InputRequired()])
    password = PasswordField('Password',validators =[InputRequired()])

class FeedbackForm(FlaskForm):
    title = StringField('Title',validators = [InputRequired()])
    content = StringField('Content',validators= [InputRequired()])


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
