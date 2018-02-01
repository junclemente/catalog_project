from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as
                         Serializer, BadSignature, SignatureExpired)
import random
import string

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits)
                     for x in xrange(32))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    picture = Column(String)
    email = Column(String)

    # For testing only
    # password_hash = Column(String(64))

    # def hash_password(self, password):
    #     self.password_hash = pwd_context.encrypt(password)

    # def verify_password(self, password):
    #     return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    # @property
    # def serialize(self):
    #     userJSON = {'username': self.username,
    #                 'email': self.email,
    #                 'id': self.id}
    #     return userJSON

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid token, but expired
            return None
        except BadSignature:
            # Invalid token
            return None
        user_id = data['id']
        return user_id


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    # description = Column(String(300))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    items = relationship("Item", cascade="all, delete-orphan")

    @property
    def serialize(self):
        categoryJSON = {'id': self.id,
                        # 'user_id': self.user_id, # for testing only
                        'name': self.name
                        }
        return categoryJSON


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)  # model name
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship(Category,
                            backref=backref("Category",
                                            cascade="all, delete-orphan"))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        itemJSON = {'id': self.id,
                    'user_id': self.user_id,  # for testing purposes
                    'name': self.name,
                    'description': self.description,
                    'category_id': self.category_id,
                    'category_name': self.category.name
                    }
        return itemJSON


engine = create_engine('sqlite:///catalogProject.db')


Base.metadata.create_all(engine)
