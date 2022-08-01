from flask import Flask, flash, make_response, render_template, redirect, \
    abort, url_for, request
from flask_ckeditor import CKEditor
from flask_login import current_user, login_user, LoginManager, logout_user, \
    login_required
from flask_wtf import CSRFProtect
import os

import config
import content as con_gen
from database import Database, User
from forms import LoginForm, RegisterForm, WriteForm


app = Flask(__name__)
csrf = CSRFProtect()
db = Database()
ckeditor = CKEditor(app)

app.secret_key = os.urandom(32)
csrf.init_app(app)

login = LoginManager(app)
login.login_view = "login"


@app.context_processor
def inject_title():
    return dict(title=config.TITLE, style=config.STYLE,
                description=config.DESCRIPTION)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", errorcode="404"), 404


@app.route("/")
@app.route("/index.html")
def index():
    content = con_gen.gen_index_string()
    return render_template("index.html", content_string=content)


@app.route("/archive")
@app.route("/archive.html")
def archive():
    entries = db.get_entries()
    content = con_gen.gen_arch_string()
    return render_template("archive.html", content_string=content)


@app.route("/user/<name>")
def user(name):
    content = con_gen.gen_user_string(name)
    if content != "":
        return render_template("user.html", name=name, content_string=content)
    abort(404)


@app.route("/entry/<ident>")
def entry(ident):
    content = con_gen.gen_stand_string(ident)
    if content != "":
        return render_template("standalone.html", content_string=content)
    abort(404)


@app.route("/feed")
@app.route("/feed.xml")
@app.route("/rss")
@app.route("/rss.xml")
def feed():
    content = con_gen.get_rss_string()
    rss_xml = render_template("rss.xml", content_string=content)
    return rss_xml


@login.user_loader
def load_user(ident):
    db_user = db.get_user_by_id(ident)
    if db_user is not None:
        return db.db_to_user(*db_user)
    return None


@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        db_user = db.get_user_by_name(form.username.data)
        if db_user is not None:
            user = db.db_to_user(*db_user)
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("index"))
        flash("Invalid username or password.")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route('/logout')
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated or not config.ALLOW_REGISTRATION:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        db_user = db.get_user_by_name(form.username.data)
        if db_user is None:
            user = User(form.username.data)
            user.set_password(form.password.data)
            ident = db.insert_user(user)
            if ident is not None:
                user.set_id(ident)
                login_user(user)
                return redirect(url_for("index"))
        flash("An error occured during registration.")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/write", methods=["GET", "POST"])
@app.route("/write.html", methods=["GET", "POST"])
@login_required
def write():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    form = WriteForm()
    print("data", form.text.data)
    print("data", request.form.get("text"))
    if form.validate_on_submit():
        db.insert_entry(form.name.data, form.date.data,
                        form.text.data, form.rating.data, current_user.id)
        return redirect(url_for("index"))
    return render_template("write.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
