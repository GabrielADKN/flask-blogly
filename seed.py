"""Seed the database."""
from models import db, connect_db, User, Post, Tag, PostTag
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

tag1 = Tag(name="Fun")
tag2 = Tag(name="Sad")
tag3 = Tag(name="Happy")
tag4 = Tag(name="Exciting")
tag5 = Tag(name="Boring")
tag6 = Tag(name="Scary")

db.session.add_all([tag1, tag2, tag3, tag4, tag5, tag6])
db.session.commit()

posttag1 = PostTag(post_id=1, tag_id=1)
posttag2 = PostTag(post_id=2, tag_id=2)
posttag3 = PostTag(post_id=3, tag_id=3)
posttag4 = PostTag(post_id=4, tag_id=4)
posttag5 = PostTag(post_id=5, tag_id=5)
posttag6 = PostTag(post_id=6, tag_id=6)
posttag7 = PostTag(post_id=7, tag_id=1)
posttag8 = PostTag(post_id=8, tag_id=2)
posttag9 = PostTag(post_id=1, tag_id=3)
posttag10 = PostTag(post_id=2, tag_id=4)
posttag11 = PostTag(post_id=2, tag_id=5)
posttag12 = PostTag(post_id=2, tag_id=6)
posttag13 = PostTag(post_id=3, tag_id=1)
posttag14 = PostTag(post_id=3, tag_id=2)
posttag15 = PostTag(post_id=4, tag_id=3)
posttag16 = PostTag(post_id=3, tag_id=4)
posttag17 = PostTag(post_id=3, tag_id=5)
posttag18 = PostTag(post_id=3, tag_id=6)
posttag19 = PostTag(post_id=4, tag_id=1)
posttag20 = PostTag(post_id=4, tag_id=2)
posttag21 = PostTag(post_id=7, tag_id=3)
posttag22 = PostTag(post_id=10, tag_id=4)
posttag23 = PostTag(post_id=4, tag_id=5)
posttag24 = PostTag(post_id=4, tag_id=6)
posttag25 = PostTag(post_id=5, tag_id=1)
posttag26 = PostTag(post_id=5, tag_id=2)
posttag27 = PostTag(post_id=5, tag_id=3)
posttag28 = PostTag(post_id=5, tag_id=4)
posttag29 = PostTag(post_id=8, tag_id=5)
posttag30 = PostTag(post_id=5, tag_id=6)

db.session.add_all([posttag1, posttag2, posttag3, posttag4, posttag5, posttag6, posttag7, posttag8, posttag9, posttag10, posttag11, posttag12, posttag13, posttag14, posttag15, posttag16, posttag17, posttag18, posttag19, posttag20, posttag21, posttag22, posttag23, posttag24, posttag25, posttag26, posttag27, posttag28, posttag29, posttag30])
db.session.commit()
