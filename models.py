"""Models for Blogly."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = (
    "https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG-File.png"
)


def connect_db(app):
    """Connect to database."""

    app.app_context().push()
    db.app = app
    db.init_app(app)


# models
class User(db.Model):
    """User."""

    __tablename__ = "users"

    @classmethod
    def find_by_firstname(cls, first_name):
        """Find user by first_name."""
        return cls.query.filter_by(first_name=first_name).first()

    @classmethod
    def find_by_id(cls, _id):
        """Find user by id."""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_or_create(cls, first_name, last_name, image_url=DEFAULT_IMAGE_URL):
        """Find or create user."""
        user = cls.find_by_firstname(first_name)
        if user:
            return user
        user = cls(
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )
        user.save_to_db()
        return user

    @classmethod
    def get_all_users(cls):
        """Get all users."""
        return cls.query.all()

    @classmethod
    def update_user(cls, _id, first_name, last_name, image_url):
        """Update user."""
        user = cls.find_by_id(_id)
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        user.save_to_db()
        return user

    @classmethod
    def delete_user(cls, _id):
        """Delete user."""
        user = cls.find_by_id(_id)
        user.delete_from_db()

    def save_to_db(self):
        """Save user to database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete user from database."""
        db.session.delete(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        """Show info about user."""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def get_full_name(self):
        """Get full name."""
        u = self
        return f"{u.first_name} {u.last_name}"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # user = db.relationship("User", backref="posts")
    tags = db.relationship("Tag", secondary="post_tags", backref="posts")

    def __repr__(self):
        """Show info about post."""
        p = self
        return f"<Post {p.id} {p.title} {p.content} {p.created_at} {p.user_id}>"

    @classmethod
    def get_all_posts(cls):
        """Get all posts."""
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        """Find post by id."""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_user_all_posts(cls, user_id):
        """Find all posts by user."""
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_or_create(cls, title, content, user_id):
        """Find or create post."""
        post = cls(
            title=title,
            content=content,
            user_id=user_id,
        )
        post.save_to_db()
        return post

    @classmethod
    def update_post(cls, _id, title, content):
        """Update post."""
        post = cls.find_by_id(_id)
        post.title = title
        post.content = content
        post.save_to_db()
        return post

    @classmethod
    def delete_post(cls, _id):
        """Delete post."""
        post = cls.find_by_id(_id)
        post.delete_from_db()

    def get_date(self):
        """Get date."""
        p = self
        return p.created_at.strftime("%b %d %Y, %I:%M %p")

    def save_to_db(self):
        """Save post to database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete post from database."""
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_recent_posts(cls):
        """Get recent posts."""
        return cls.query.order_by(cls.created_at.desc()).limit(5).all()


class Tag(db.Model):
    """Tag model."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # posts = db.relationship("Post", secondary="post_tags", backref="tags")

    def __repr__(self):
        """Show info about tag."""
        t = self
        return f"<Tag {t.id} {t.name}>"

    @classmethod
    def get_all_tags(cls):
        """Get all tags."""
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        """Find tag by id."""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_name(cls, name):
        """Find tag by name."""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_or_create(cls, name):
        """Find or create tag."""
        tag = cls.find_by_name(name)
        if tag:
            return tag
        tag = cls(
            name=name,
        )
        tag.save_to_db()
        return tag

    @classmethod
    def update_tag(cls, _id, name):
        """Update tag."""
        tag = cls.find_by_id(_id)
        tag.name = name
        tag.save_to_db()
        return tag

    @classmethod
    def delete_tag(cls, _id):
        """Delete tag."""
        tag = cls.find_by_id(_id)
        tag.delete_from_db()

    def save_to_db(self):
        """Save tag to database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete tag from database."""
        db.session.delete(self)
        db.session.commit()


class PostTag(db.Model):
    """PostTag model."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        """Show info about post_tag."""
        pt = self
        return f"<PostTag {pt.post_id} {pt.tag_id}>"

    @classmethod
    def get_all_post_tags(cls):
        """Get all post_tags."""
        return cls.query.all()

    @classmethod
    def find_by_post_id(cls, post_id):
        """Find post_tag by post_id."""
        return cls.query.filter_by(post_id=post_id).all()

    @classmethod
    def find_by_tag_id(cls, tag_id):
        """Find post_tag by tag_id."""
        return cls.query.filter_by(tag_id=tag_id).all()

    @classmethod
    def find_by_post_tag(cls, post_id, tag_id):
        """Find post_tag by post_id and tag_id."""
        return cls.query.filter_by(post_id=post_id, tag_id=tag_id).first()

    @classmethod
    def find_or_create(cls, post_id, tag_id):
        """Find or create post_tag."""
        post_tag = cls(
            post_id=post_id,
            tag_id=tag_id,
        )
        post_tag.save_to_db()
        return post_tag

    @classmethod
    def delete_post_tag(cls, post_id, tag_id):
        """Delete post_tag."""
        post_tag = cls.find_by_post_tag(post_id, tag_id)
        post_tag.delete_from_db()

    def save_to_db(self):
        """Save post_tag to database."""
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """Delete post_tag from database."""
        db.session.delete(self)
        db.session.commit()
