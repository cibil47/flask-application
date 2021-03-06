from application import bcrypt, db
from flask import render_template, url_for, flash, redirect, request,Blueprint
from application.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from application.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from application.users.utils import save_file,check_username,check_email

users = Blueprint("users",__name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        if check_username(request.form.get("username")) == "true":
            flash("Username is already taken.Please choose another one!!","danger")
            return redirect(url_for("users.register"))
        if check_email(request.form.get("email")) == "true":
            flash("Email is already taken.Plaese choose another one!!", "danger")
            return redirect(url_for("users.register"))
        hashed_password = bcrypt.generate_password_hash(request.form.get("password")).decode("utf-8")
        user = User(username=request.form.get("username"), email=request.form.get("email"), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!!", "success")
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        print(request.form)
        user = User.query.filter_by(email=request.form.get("email")).first()
        if user and bcrypt.check_password_hash(user.password, request.form.get("password")):
            login_user(user, remember=request.form.get("remember_me"))
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login unsuccessful Please check your email or password", "danger")
    return render_template("login.html", title="Login")


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_file(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/{}".format(current_user.image_file))
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<username>")
def user_posts(username):
    username = str(username)
    page_no = request.args.get("page",1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(per_page=3,page=page_no)
    return render_template("user_posts.html", posts=posts,user = user)