from flask import Flask, flash, make_response, render_template, request, redirect, abort, url_for
from flask_login import current_user, login_user, LoginManager, logout_user

import content as con_gen
import config

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

TITLE = config.TITLE
STYLE = config.STYLE
DESCRIPTION = config.DESCRIPTION
WEBSITE = config.WEBSITE

from werkzeug.security import generate_password_hash, check_password_hash

class User():

    def __init__(self, username):
        self.username = username
        self.id = 1
        self.is_active = True
        self.is_authenticated = False
        self.is_anonymous = False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

u = User("marten")
u.set_password("test")

class Config(object):
    SECRET_KEY = "123534"

app.config.from_object(Config)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", title=TITLE, errorcode="404", style=STYLE), 404


@app.route("/")
@app.route("/index.html")
def index():
    content = con_gen.gen_index_string()
    return render_template("index.html", title=TITLE, content_string=content, style=STYLE)


@app.route("/archive")
@app.route("/archive.html")
def blog_archive():
    content = con_gen.gen_arch_string()
    return render_template("archive.html", title=TITLE, content_string=content, style=STYLE)


@app.route("/entry/<path>")
def entry(path):
    content = con_gen.gen_stand_string(path)
    if content != "":
        return render_template("standalone.html", title=TITLE, content_string=content, style=STYLE)
    abort(404)


@app.route("/feed.xml")
@app.route("/rss.xml")
def feed():
    content = con_gen.get_rss_string()
    rss_xml = render_template("rss.xml", content_string=content, title=TITLE,
                              description=DESCRIPTION, website=WEBSITE)
    response = make_response(rss_xml)
    response.headers["Content-Type"] = "application/rss+xml"
    return response

@login.user_loader
def load_user(id):
    ## TODO: load user from db by id
    return id

@app.route("/login", methods=["GET", "POST"])
def login():
    #if current_user.is_authenticated:
    #    return redirect("/index")
    form = LoginForm()
    if form.validate_on_submit():
        user = u
        #user = form.username.data
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title="Sign In", form=form, style=STYLE)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
