from unittest import TestCase

from models import db, connect_db, User, Post
from app import app

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        """Test that user appears on the users list page."""

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_show_user(self):
        """Test that user appears on the user detail page."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>User number {self.user_id}</h1>", html)

    def test_add_user(self):
        """Test that user can be added."""

        with app.test_client() as client:
            d = {
                "first_name": "Test2",
                "last_name": "User2",
                "image": "https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG-File.png",
            }
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            print(f"Response Status Code: {resp.status_code}")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>User number 2</h1>", html)

    def test_edit_user(self):
        """Test that user can be edited."""

        with app.test_client() as client:
            d = {"first_name": "Test2", "last_name": "User2", "image": ""}
            resp = client.post(
                f"/users/{self.user_id}/edit", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test2", html)

    def test_delete_user(self):
        """Test that user can be deleted."""

        with app.test_client() as client:
            resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("<h1>Test User</h1>", html)


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        Post.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(
            title="Test Post", content="This is a test post.", user_id=self.user_id
        )
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_post(self):
        """Test that post appears on the post detail page."""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"<h1>Test Post</h1>", html)

    def test_add_post(self):
        """Test that post can be added."""

        with app.test_client() as client:
            d = {
                "title": "Test Post 2",
                "content": "This is a test post.",
                "user_id": self.user_id,
            }
            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f"{d['title']}", html)

    def test_edit_post(self):
        """Test that post can be edited."""

        with app.test_client() as client:
            d = {
                "title": "Test Post 2",
                "content": "This is a test post.",
                "user_id": self.user_id,
            }
            resp = client.post(
                f"/posts/{self.post_id}/edit", data=d, follow_redirects=True
            )
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test Post 2", html)

    def test_delete_post(self):
        """Test that post can be deleted."""

        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(f"Test Post 1", html)
