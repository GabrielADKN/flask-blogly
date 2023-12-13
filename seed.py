"""Seed the database."""
from models import db, connect_db, User, Post
from app import app

# Create all tables
db.drop_all()
db.create_all()

#if table isn't empty, delete all rows
User.query.delete()

# Add users
john = User.find_or_create(first_name="John", last_name="Tester")
Jane = User.find_or_create(first_name="Jane", last_name="Leveler", image_url="https://www.pngall.com/wp-content/uploads/12/Avatar-Profile-Vector-PNG-Photos.png")
Olivier = User.find_or_create(first_name="Oliver", last_name="Denver", image_url="https://freesvg.org/img/1547510251.png")
Jennifer = User.find_or_create(first_name="Jennifer", last_name="Doe", image_url="https://cdn1.iconfinder.com/data/icons/female-avatars-vol-1/256/female-portrait-avatar-profile-woman-sexy-afro-2-1024.png")

# Add new objects to session, so they'll persist
db.session.add(john)
db.session.add(Jane)
db.session.add(Olivier)
db.session.add(Jennifer)

# Commit changes
db.session.commit()

post1 = Post(title="First Post", content="This is the first post ever!", user_id=1)
post2 = Post(title="Second Post", content="This is the second post ever!", user_id=1)
post3 = Post(title="Third Post", content="This is the third post ever!", user_id=1)
post4 = Post(title="Fourth Post", content="This is the fourth post ever!", user_id=1)

post5 = Post(title="First Post", content="This is the first post ever!", user_id=2)
post6 = Post(title="Second Post", content="This is the second post ever!", user_id=2)
post7 = Post(title="Third Post", content="This is the third post ever!", user_id=2)
post8 = Post(title="Fourth Post", content="This is the fourth post ever!", user_id=2)

post9 = Post(title="First Post", content="This is the first post ever!", user_id=4)
post10 = Post(title="Second Post", content="This is the second post ever!", user_id=4)
post11 = Post(title="Third Post", content="This is the third post ever!", user_id=4)
post12 = Post(title="Fourth Post", content="This is the fourth post ever!", user_id=4)

post13 = Post(title="First Post", content="This is the first post ever!", user_id=3)
post14 = Post(title="Second Post", content="This is the second post ever!", user_id=3)
post15 = Post(title="Third Post", content="This is the third post ever!", user_id=3)
post16 = Post(title="Fourth Post", content="This is the fourth post ever!", user_id=3)

db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8, post9, post10, post11, post12, post13, post14, post15, post16])
db.session.commit()
