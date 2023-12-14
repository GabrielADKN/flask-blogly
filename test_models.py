from unittest import TestCase

from app import app
from models import db, connect_db, User, Post

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """ "Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_get_full_name(self):
        """Test that get_full_name works."""

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.get_full_name(), "Test User")

    def test_get_all_users(self):
        """Test that get_all_users works."""

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.get_all_users(), [user])

    def test_find_by_id(self):
        """Test that find_by_id works."""

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.find_by_id(user.id), user)

    def test_find_by_firstname(self):
        """Test that find_by_firstname works."""

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.find_by_firstname(user.first_name), user)

    def test_find_or_create(self):
        """Test that find_or_create works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        self.assertEqual(User.find_by_id(user.id), user)

    def test_update_user(self):
        """Test that update_user works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        user = User.update_user(
            user.id,
            "Test",
            "User",
            "https://www.pngall.com/wp-content/uploads/12/Avatar-Profile-Vector-PNG-Photos.png",
        )
        db.session.commit()

        self.assertEqual(User.find_by_id(user.id), user)

    def test_delete_user(self):
        """Test that delete_user works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        User.delete_user(user.id)
        db.session.commit()

        self.assertEqual(User.query.all(), [])


class PostModelTestCase(TestCase):
    """Tests for model for Posts."""

    def setUp(self):
        """Clean up any existing posts."""

        User.query.delete()
        Post.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_find_by_id(self):
        """Test that find_by_id works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        post = Post(title="Test", content="Test", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.assertEqual(Post.find_by_id(post.id), post)

    def test_find_user_all_posts(self):
        """Test that find_user_all_posts works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        post = Post(title="Test", content="Test", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        self.assertEqual(Post.find_user_all_posts(user.id), [post])

    def test_update_post(self):
        """Test that update_post works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        post = Post(title="Test", content="Test", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        post = Post.update_post(post.id, "Test", "Test")
        db.session.commit()

        self.assertEqual(Post.find_by_id(post.id), post)

    def test_delete_post(self):
        """Test that delete_post works."""

        user = User.find_or_create(first_name="Test", last_name="User")
        db.session.commit()

        post = Post(title="Test", content="Test", user_id=user.id)
        db.session.add(post)
        db.session.commit()

        Post.delete_post(post.id)
        db.session.commit()

        self.assertEqual(Post.query.all(), [])
