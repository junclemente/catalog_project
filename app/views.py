from app import app

from flask import render_template

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Category, Item


engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def index():
    category = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).all()
    return render_template('index.html', category=category, items=items)


@app.route('/category_list/<int:cat_id>')
def category_list(cat_id):
    category = session.query(Category).filter_by(id=cat_id).one()
    items = session.query(Item).filter_by(category_id=cat_id).all()
    return render_template('category_list.html', category=category,
                           items=items)
