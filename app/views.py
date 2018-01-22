from app import app

from flask import render_template, flash, redirect, url_for

from forms import CategoryForm

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


@app.route('/item/<int:item_id>')
def item(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    return render_template('item.html', item=item)


@app.route('/addCategory', methods=['GET', 'POST'])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        new_category = Category(name=name,
                                description=description)
        session.add(new_category)
        session.commit()
        flash('New Category Added')
        return redirect(url_for('index'))
    return render_template('add_category.html', form=form)
