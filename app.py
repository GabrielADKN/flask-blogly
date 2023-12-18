"""Blogly application."""

from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    recent_post = Post.get_recent_posts()
    return render_template("index.html", posts=recent_post)
    # return redirect(url_for("all_users"))


@app.route("/users")
def all_users():
    users = User.get_all_users()
    return render_template("users/users.html", users=users)


@app.route("/users/<int:user_id>")
def user(user_id):
    user = User.find_by_id(user_id)
    posts = Post.find_user_all_posts(user_id)
    return render_template("users/details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def show_edit(user_id):
    user = User.find_by_id(user_id)
    return render_template("users/edit.html", user=user)


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
    return render_template("users/delete.html", user=user)


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
        return render_template("users/new.html")


@app.route("/users/<int:user_id>/posts/new", methods=["GET", "POST"])
def new_post(user_id):
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        tags = request.form.getlist("tags")
        
        post = Post.find_or_create(title, content, user_id)
        
        for tag in tags:
            PostTag.find_or_create(post.id, tag)
        
        return redirect(url_for("user", user_id=user_id, post=post))
    else:
        user = User.find_by_id(user_id)
        tags = Tag.get_all_tags()
        return render_template("posts/new_post.html", user=user, tags=tags)


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.find_by_id(post_id)

    return render_template("posts/post_details.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.find_by_id(post_id)
    user = User.find_by_id(post.user_id)
    tags = Tag.get_all_tags()
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        post = Post.update_post(post_id, title, content)
        tags = request.form.getlist("tags")
        print("#############################################")
        print(tags)
        for tag in post.tags:
            if tag.id not in tags:
                PostTag.delete_post_tag(post.id, tag.id)

        for tag in tags:
            if tag not in post.tags:
                PostTag.find_or_create(post.id, tag)

        return redirect(url_for("show_post", post_id=post.id, user=user))
    else:
        return render_template("posts/edit_post.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/delete", methods=["GET", "POST"])
def delete_post(post_id):
    post = Post.find_by_id(post_id)
    user = User.find_by_id(post.user_id)
    if request.method == "POST":
        Post.delete_post(post.id)
        return redirect(url_for("user", user_id=user.id))
    else:
        return render_template("posts/delete_post.html", post=post, user=user)

@app.route("/tags")
def show_tags():
    tags = Tag.get_all_tags()
    return render_template("tags/tags.html", tags=tags)

@app.route("/tags/new", methods=["GET", "POST"])
def new_tag():
    if request.method == "POST":
        name = request.form["name"]
        tag = Tag.find_or_create(name)
        return redirect(url_for("show_tags"))
    else:
        return render_template("tags/new_tag.html")

@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    tag = Tag.find_by_id(tag_id)
    return render_template("tags/tag_details.html", tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["GET", "POST"])
def edit_tag(tag_id):
    tag = Tag.find_by_id(tag_id)
    if request.method == "POST":
        name = request.form["name"]
        tag = Tag.update_tag(tag_id, name)
        return redirect(url_for("show_tag", tag_id=tag.id))
    else:
        return render_template("tags/edit_tag.html", tag=tag)
    
@app.route("/tags/<int:tag_id>/delete", methods=["GET", "POST"])
def delete_tag(tag_id):
    tag = Tag.find_by_id(tag_id)
    if request.method == "POST":
        Tag.delete_tag(tag.id)
        return redirect(url_for("show_tags"))
    else:
        return render_template("tags/delete_tag.html", tag=tag)