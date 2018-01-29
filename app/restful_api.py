from app import app

from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item


engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# For testing only
# @app.route('/api/users')
# def userJSON():
#     users = session.query(User).all()
#     return jsonify(users = [u.serialize for u in users])


@app.route('/api/allcategories')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [c.serialize for c in categories])


@app.route('/api/itemsincategory/<int:cat_id>')
def itemsInCatJSON(cat_id):
    items = session.query(Item).filter_by(category_id=cat_id).all()
    return jsonify(items = [i.serialize for i in items])


@app.route('/api/allitems')
def allItemsJSON():
    items = session.query(Item).all()
    return jsonify(items = [i.serialize for i in items])


@app.route('/api/item/<int:id>')
def itemJSON(id):
    items = session.query(Item).filter_by(id=id).first()
    return jsonify(items.serialize)
