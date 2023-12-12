"""Models for Blogly."""

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

    def __repr__(self):
        """Show info about user."""
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def get_full_name(self):
        """Get full name."""
        u = self
        return f"{u.first_name} {u.last_name}"