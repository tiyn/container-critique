from flask import Flask, flash, make_response, render_template, request, redirect, abort, url_for
from flask_login import current_user, login_user, LoginManager, logout_user
from flask_wtf import CSRFProtect

import content as con_gen
import config


app = Flask(__name__)
csrf = CSRFProtect()
app.secret_key = "123534"
csrf.init_app(app)

login = LoginManager(app)
login.login_view = "login"

TITLE = config.TITLE
STYLE = config.STYLE
DESCRIPTION = config.DESCRIPTION
WEBSITE = config.WEBSITE

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
def archive():
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
def load_user(ident):
    ## TODO: load user from db by id
    db_user = db.get_by_id(ident)
    if db_user is not None:
        return db.db_to_user(*db_user)
    return None

from login import LoginForm, User
from database import Database

db = Database()

@app.route("/login", methods=["GET", "POST"])
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        db_user = db.get_by_name(form.username.data)
        if db_user is None:
            flash("Invalid username or password")
            return redirect(url_for("login"))
        user = db.db_to_user(*db_user)
        if not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("index"))
    return render_template("login.html", title=TITLE, form=form, style=STYLE)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")
