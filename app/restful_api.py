from app import app

from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item


engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/categoryJSON')
@app.route('/categoryjson')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [c.serialize for c in categories])


@app.route('/itemJSON/<int:id>')
@app.route('/itemjson/<int:id>')
def itemJSON(id):
    items = session.query(Item).filter_by(category_id=id).all()
    return jsonify(items = [i.serialize for i in items])
