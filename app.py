"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "mysecretkey"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()


@app.route("/")
def index():
    # users = User.get_all_users()
    return redirect(url_for("all_users"))


@app.route("/users")
def all_users():
    users = User.get_all_users()
    return render_template("home.html", users=users)


@app.route("/users/<int:user_id>")
def user(user_id):
    user = User.find_by_id(user_id)
    posts = Post.find_user_all_posts(user_id)
    return render_template("details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    user = User.find_by_id(user_id)
    return render_template("edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit(user_id):
    db.session.rollback()
    user = User.find_by_id(user_id)
    if user:
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image"]
        user = User.update_user(user_id, first_name, last_name, image_url)
        # user.save_to_db()
        return redirect(url_for("user", user_id=user.id))
    else:
        abort(404)


@app.route("/users/<int:user_id>/delete")
def delete_show(user_id):
    user = User.find_by_id(user_id)
    return render_template("delete.html", user=user)


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete(user_id):
    user = User.find_by_id(user_id)
    if user:
        User.delete_user(user.id)
        return redirect(url_for("all_users"))
    else:
        abort(404)


@app.route("/users/new", methods=["GET", "POST"])
def new_user():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        image_url = request.form["image"]
        user = User.find_or_create(first_name, last_name, image_url)
        # user.save_to_db()
        return redirect(url_for("user", user_id=user.id))
    else:
        return render_template("new.html")

@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def new_post(user_id):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post.find_or_create(title, content, user_id)
        return redirect(url_for("user", user_id=user_id, post=post))
    else:
        user = User.find_by_id(user_id)
        return render_template("new_post.html", user=user)

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.find_by_id(post_id)
    user = User.find_by_id(post.user_id)
    return render_template("post_details.html", post=post, user=user)

@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.find_by_id(post_id)
    user = User.find_by_id(post.user_id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post.update_post(post_id, title, content)
        return redirect(url_for("show_post", post_id=post.id, user=user))
    else:
        return render_template("edit_post.html", post=post, user=user)
    
@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = Post.find_by_id(post_id)
    user = User.find_by_id(post.user_id)
    if request.method == "POST":
        Post.delete_post(post.id)
        return redirect(url_for("user", user_id=user.id))
    else:
        return render_template("delete_post.html", post=post, user=user)