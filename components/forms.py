from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models.user_model import UserModel


class SignupForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=25)])

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField("SignUp")

    def validate_username(self, username):
        user = UserModel.find_by_username(username.data)
        if user:
            raise ValidationError("username is taken")



class LoginForm(FlaskForm):
    username = StringField('Username',
                            validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])
    
    submit = SubmitField("Login")


class TasksForm(FlaskForm):
    title = StringField('Title',
                            validators=[DataRequired()])

    description = TextAreaField("Description")
    
    submit = SubmitField("Add Task")