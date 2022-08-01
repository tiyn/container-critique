from datetime import date
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired, \
    NumberRange, ValidationError, Length


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=4, max=32)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=4, max=32)])
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=4, max=32)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=4, max=32)])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class WriteForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),
                                           Length(min=2, max=64)])
    date = IntegerField("Release Year", default=date.today().year, validators=[
        DataRequired(), NumberRange(min=0, max=date.today().year,
                                    message="Year has to be valid.")])
    text = CKEditorField("Text", validators=[DataRequired()])
    rating = IntegerField("Rating", default=50, validators=[InputRequired(
    ), NumberRange(min=0, max=100, message="Number has to be between 0 and 100.")])
    submit = SubmitField("Publish")

    def validate_text(self, text):
        if "<h1>" in text.data or "</h1>" in text.data:
            raise ValidationError("Headings on level 1 are not permitted.")
