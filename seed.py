"""Seed the database."""
from models import db, connect_db, User
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