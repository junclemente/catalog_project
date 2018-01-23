from app import app

from flask import render_template, flash, redirect, url_for, request

from forms import CategoryAddForm, CategoryEditForm, ConfirmForm, ItemForm

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


@app.route('/addCategory', methods=['GET', 'POST'])
def add_category():
    form = CategoryAddForm()
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
    items = session.query(Item).filter_by(category_id=cat_id).all()
    if form.validate_on_submit():
        session.delete(category)
        if items:
            for item in items:
                session.delete(item)
        session.commit()
        flash("Category deleted.")
        return redirect(url_for('index'))
    return render_template('delete_category.html',
                           category=category,
                           items=items,
                           form=form)


@app.route('/edit_category/<int:cat_id>', methods=['GET', 'POST'])
def edit_category(cat_id):
    form = CategoryEditForm()
    category = session.query(Category).filter_by(id=cat_id).one()
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        flash('Category has been edited successfully.')
        return render_template('category_list.html', category=category)
    if request.method == 'GET':
        form.name.data = category.name
        form.description.data = category.description
    return render_template('edit_category.html', category=category, form=form)


@app.route('/item/<int:item_id>')
def item(item_id):
    item = session.query(Item).filter_by(id=item_id).first()
    return render_template('item.html', item=item)


@app.route('/add_item/<int:cat_id>', methods=['GET', 'POST'])
def add_item(cat_id):
    form = ItemForm()
    category = session.query(Category).filter_by(id=cat_id).first()
    if form.validate_on_submit():
        new_item = Item(name=form.name.data,
                        description=form.description.data,
                        category_id=cat_id)
        session.add(new_item)
        session.commit()
        flash('Item added successfully.')
        return redirect(url_for('category_list', cat_id=category.id))
    return render_template('add_item.html', category=category, form=form)


@app.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    form = ConfirmForm()
    item = session.query(Item).filter_by(id=item_id).first()
    if form.validate_on_submit():
            session.delete(item)
            session.commit()
            flash('Item successfully deleted.')
            return redirect(url_for('index'))
    return render_template('delete_item.html', item=item, form=form)


# def edit_item(item_id):
