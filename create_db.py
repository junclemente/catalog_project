#!/usr/bin/env python
"""
This file was used to initialize a database for this project for testing
purposes only.
"""
from app import app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from app.models import User, Category, Item, Base


engine = create_engine('sqlite:///catalogProject.db')
# Bind the engine to the metadata of the Base class so that decleratives can
# be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# DBSession() instance establishes all converstations with the DB and
# represents a staging zone for all ojbects loaded into the DB session object.
# Any change made against the objects in the session won't be persisted into
# the DB until it is commited by calling: session.commit(). Changes can be
# reverted to the last commit by calling: session.rollback()
session = DBSession()

# For testing, assign an email address
TEST_USER_EMAIL_1 = 'test@test.com'
TEST_USER_EMAIL_2 = 'Edit@ThisEmailAddress.com'

# Create 'master' user.
user1 = User(username=TEST_USER_EMAIL_1,
             email=TEST_USER_EMAIL_1)
# user1.hash_password("12345")
session.add(user1)
session.commit()
print "Created user: " + TEST_USER_EMAIL_1

user2 = User(username=TEST_USER_EMAIL_2,
             email=TEST_USER_EMAIL_2)
session.add(user2)
session.commit()
print "Created user: " + TEST_USER_EMAIL_2


# Create initial category
category1 = Category(name="Snowboard",
                     user_id="1")
session.add(category1)
session.commit()

# category2 = Category(name="Skiing",
#                      user_id="1")
# session.add(category2)
# session.commit()

category2 = Category(name="Foosball",
                     user_id="2")
session.add(category2)
session.commit()

# category4 = Category(name="Football",
#                      user_id="2")
# session.add(category4)
# session.commit()


# Create initial item
item1 = Item(name="Merc",
             category_id="1",
             user_id="1",
             description="Beginner to Intermediate snowboard.")
session.add(item1)
session.commit()

item2 = Item(name="Aero Coiler Boa",
             category_id="1",
             user_id="1",
             description="Snowboard Boots, 2017")
session.add(item2)
session.commit()

item3 = Item(name="Five Hybrid Snowboard Bindings",
             category_id="1",
             user_id="1",
             description="Snowboard Bindings")
session.add(item3)
session.commit()


item4 = Item(name="Foosball Ball",
             category_id="2",
             user_id="2",
             description="Game ball")
session.add(item4)
session.commit()

item5 = Item(name="Foosball Gloves",
             category_id="2",
             user_id="2",
             description="Gloves")
session.add(item5)
session.commit()

print "Created categories and items"
