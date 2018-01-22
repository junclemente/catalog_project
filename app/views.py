from app import app

from flask import render_template, flash, redirect, url_for

from forms import CategoryForm, ConfirmForm, ItemForm

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


@app.route('/delete_category/<int:cat_id>', methods=['GET', 'POST'])
def delete_category(cat_id):
    form = ConfirmForm()
    category = session.query(Category).filter_by(id=cat_id).first()
    if form.validate_on_submit():
        session.delete(category)
        session.commit()
        flash("Category deleted.")
        return redirect(url_for('index'))
    return render_template('delete_category.html',
                           category=category,
                           form=form)


@app.route('/add_item/<int:cat_id>', methods=['GET', 'POST'])
def add_item(cat_id):
    form = ItemForm()
    if form.validate_on_submit():
        new_item = Item(name=form.name.data,
                        # maker=form.maker.data,
                        # model_year=form.model_year.data,
                        description=form.description.data,
                        category_id=cat_id)
        session.add(new_item)
        session.commit()
        flash('Item added successfully.')
        return redirect(url_for('index'))
    return render_template('add_item.html', cat_id=cat_id,form=form)
