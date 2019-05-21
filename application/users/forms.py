from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from application.models import User

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired() ,Length(min=4 ,max=10)])
    email = StringField("Email", validators=[DataRequired() ,Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self ,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken.Plaese choose another one")

    def validate_email(self ,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already taken.Plaese choose another one")

class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired() ,Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired() ,Length(min=4 ,max=10)])
    email = StringField("Email", validators=[DataRequired() ,Email()])
    picture = FileField("Update profile picture" ,validators=[FileAllowed(["jpg" ,"png" ,"jpeg"])])
    submit = SubmitField("Update")

    def validate_username(self ,username):
        if username != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken.Plaese choose another one")

    def validate_email(self ,email):
        if email != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email is already taken.Plaese choose another one")