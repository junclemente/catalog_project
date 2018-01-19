from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models import User, Category, Item, Base


engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


user1 = User(username="master")
session.add(user1)
session.commit()
print "Created user: 'master', password: '12345'"


category1 = Category(name="Snowboard",
                     user_id="1",
                     description="Snowboarding is a recreational activity...")
session.add(category1)
session.commit()


item1 = Item(name="Flow Merc",
             category_id="1",
             user_id="1",
             description="Beginner to Intermediate snowboard.")
session.add(item1)
session.commit()
print "Created category and item"

