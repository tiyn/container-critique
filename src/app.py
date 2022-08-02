from flask import Flask, flash, render_template, redirect, abort, url_for
from flask_ckeditor import CKEditor
from flask_login import current_user, login_user, LoginManager, logout_user, \
    login_required
from flask_wtf import CSRFProtect
import os

import config
from content import rating_to_star
from database import Database
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
    return dict(title=config.TITLE, style=config.STYLE, \
                description=config.DESCRIPTION, \
                registration=config.ALLOW_REGISTRATION, r_to_star=rating_to_star)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html", errorcode="404"), 404


@app.route("/")
def index():
    entries = db.get_entries()
    entries.reverse()
    return render_template("index.html", entries=entries)


@app.route("/archive")
def archive():
    entries = db.get_entries()
    entries.sort(key=lambda y: y.item.name)
    entries.reverse()
    entries.sort(key=lambda y: y.item.date)
    entries.reverse()
    return render_template("archive.html", entries=entries)


@app.route("/user/<name>")
def user(name):
    entries = db.get_entries_by_user(name)
    entries.sort(key=lambda y: y.item.name)
    entries.reverse()
    entries.sort(key=lambda y: y.item.date)
    entries.reverse()
    if entries != []:
        return render_template("user.html", name=name, entries=entries)
    abort(404)


@app.route("/entry/<ident>")
def entry(ident):
    entry = db.get_entry_by_id(ident)
    if entry is not None:
        return render_template("standalone.html", entry=entry)
    abort(404)


@app.route("/feed")
def feed():
    entries = db.get_entries()
    entries.reverse()
    rss_xml = render_template("rss.xml", entries=entries)
    return rss_xml


@login.user_loader
def load_user(ident):
    user = db.get_user_by_id(ident)
    if user is not None:
        return user
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.get_user_by_name(form.username.data)
        print(user)
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for("index"))
        flash("Invalid username or password.")
        return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated or not config.ALLOW_REGISTRATION:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.get_user_by_name(form.username.data)
        if user is None:
            ident = db.insert_user(form.username.data, form.password.data)
            if ident is not None:
                user = db.get_user_by_id(ident)
                login_user(user)
                return redirect(url_for("index"))
        flash("An error occured during registration.")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@app.route("/write_entry", methods=["GET", "POST"])
@login_required
def write_entry():
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    form = WriteForm()
    if form.validate_on_submit():
        db.insert_entry(form.name.data, form.date.data,
                        form.text.data, form.rating.data, current_user.id)
        return redirect(url_for("index"))
    return render_template("write.html", form=form)


@app.route("/delete_entry/<ident>", methods=["GET", "POST"])
@login_required
def delete_entry(ident):
    if not current_user.is_authenticated:
        return redirect(url_for("index"))
    if current_user.id == db.get_entry_by_id(ident).user.id:
        db.delete_entry(ident)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0")
