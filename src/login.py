from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

from werkzeug.security import generate_password_hash, check_password_hash


class User():

    def __init__(self, name, pass_hash=None):
        self.name = name
        self.id = 0
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False
        self.pass_hash = pass_hash

    def set_password(self, password):
        self.pass_hash = generate_password_hash(password)

    def set_id(self, ident):
        self.id = ident

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def get_id(self):
        return self.id

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
