from datetime import date
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired, EqualTo, InputRequired, \
    NumberRange, ValidationError, Length


class LoginForm(FlaskForm):
    """
    A Class for the Form that is used while logging in.
    """
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=4, max=32)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=4, max=32)])
    submit = SubmitField("Sign In")


class RegisterForm(FlaskForm):
    """
    A Class for the Form that is used while registering.
    """
    username = StringField("Username", validators=[DataRequired(),
                                                   Length(min=4, max=32)])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     Length(min=4, max=32)])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class SearchForm(FlaskForm):
    """
    A Class for the Form that is used while searching.
    """
    query_str = TextField(
        "Query", [DataRequired("Please enter the search term")])
    submit = SubmitField("Search")


class WriteForm(FlaskForm):
    """
    A Class for the Form that is used while writing a new entry.
    """
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
        """
        Validate a given input for html level one headers.

        Parameters:
        text (str): text to validate

        Returns:
        None

        Raises:
        ValidatenError: if the text contains a first level html tag
        """
        if "<h1>" in text.data or "</h1>" in text.data:
            raise ValidationError("Headings on level 1 are not permitted.")
