from app import app

from flask import render_template, flash, redirect, url_for, request
from flask import session as login_session

from forms import CategoryForm, CategoryEditForm, ConfirmForm
from forms import ItemForm, ItemEditForm

from catalog_db import session
from models import Category, Item

from functools import wraps


def login_required(f):
    '''
    Decorator function to ensure user is logged in prior to accessing
    certain pages.
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            flash('You must be logged in to access this page.',
                  'flash-warning')
            return redirect(url_for('show_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
@app.route('/index')
def index():
    # Categories is used to populate the categories column on the page.
    # This is the same for all routes.
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).limit(10).all()
    return render_template('index.html', categories=categories, items=items)


@app.route('/category_list/<int:cat_id>')
def category_list(cat_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=cat_id).one()
    items = session.query(Item).filter_by(category_id=cat_id).all()
    # Determines if logged-in user is the owner of the entry. If owner is true,
    # then a page with editing capabilities is provided. Otherwise, a page
    # without editing capabilities is provided.
    # This is the same for all routes that require manipulating the database.
    if ('user_id' in login_session and
            category.user_id == login_session['user_id']):
        return render_template('category_list.html',
                               categories=categories,
                               category=category,
                               items=items)
    else:
        return render_template('pub_category_list.html',
                               categories=categories,
                               category=category,
                               items=items)


@app.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    categories = session.query(Category).all()
    if form.validate_on_submit():
        name = form.name.data
        new_category = Category(name=name,
                                user_id=login_session['user_id'])
        session.add(new_category)
        session.commit()
        flash('New Category Added', "flash-success")
        return redirect(url_for('category_list', cat_id=new_category.id))
    return render_template('add_category.html', categories=categories,
                           form=form)


@app.route('/delete_category/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def delete_category(cat_id):
    form = ConfirmForm()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=cat_id).first()
    items = session.query(Item).filter_by(category_id=cat_id).all()
    # Flask-WTF and WTForms is used to manage form creation and to provide
    # CSRF protection
    if form.validate_on_submit():
        session.delete(category)
        # If there are items in this category, they will be also deleted
        # from the database.
        # Implemented cascade property in models.py therefore this is no
        # longer necessary.
        # if items:
        #     for item in items:
        #         session.delete(item)
        session.commit()
        flash("Category deleted successfully.", "flash-success")
        return redirect(url_for('index'))
    if (category.user_id != login_session['user_id']):
        flash("You must be the owner to delete this category.",
              "flash-warning")
        return redirect(url_for('category_list', cat_id=category.id))
    else:
        return render_template('delete_category.html',
                               categories=categories,
                               category=category,
                               items=items,
                               form=form)


@app.route('/edit_category/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def edit_category(cat_id):
    form = CategoryEditForm()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=cat_id).one()
    if category.user_id != login_session['user_id']:
        flash("You must be the owner to edit this category.", "flash-warning")
        return redirect(url_for('category_list', cat_id=category.id))
    if form.validate_on_submit():
        category.name = form.name.data
        flash('Category has been edited successfully.', "flash-success")
        return redirect(url_for('category_list', cat_id=category.id))
    if request.method == 'GET':
        form.name.data = category.name
    return render_template('edit_category.html', categories=categories,
                           category=category, form=form)


@app.route('/item/<int:item_id>')
def item(item_id):
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id=item_id).first()
    if ('user_id' in login_session and
            item.user_id == login_session['user_id']):
        return render_template('item.html', categories=categories, item=item)
    else:
        return render_template('pub_item.html', categories=categories,
                               item=item)


@app.route('/add_item/<int:cat_id>', methods=['GET', 'POST'])
@login_required
def add_item(cat_id):
    form = ItemForm()
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=cat_id).first()
    if form.validate_on_submit():
        new_item = Item(name=form.name.data,
                        description=form.description.data or "No description",
                        category_id=category.id,
                        user_id=login_session['user_id'])
        print new_item
        session.add(new_item)
        session.commit()
        flash('Item added successfully.', "flash-success")
        return redirect(url_for('category_list', cat_id=category.id))
    return render_template('add_item.html', categories=categories,
                           category=category, form=form)


@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    form = ItemEditForm()
    item = session.query(Item).filter_by(id=item_id).one()

    if item.user_id != login_session['user_id']:
        flash("You must be the owner to make changes to this item.",
              "flash-warning")
        return redirect(url_for('item', item_id=item.id))

    # The choices for the dropdown selectfield is dynamically populated by
    # querying the Category table.
    categories = session.query(Category).all()

    # The default value of the selectfield is also dynamically set.
    category = session.query(Category).all()
    select_field = [(c.id, c.name) for c in category]
    if request.method == 'POST':
        item.name = form.name.data
        item.description = form.description.data
        item.category_id = form.category_id.data
        session.commit()
        flash('Item edited successfully.', "flash-success")
        return redirect(url_for('item', item_id=item.id))
    if request.method == 'GET':

        # Dynamically assigned selectfield and default value is assigned
        form.category_id.choices = select_field
        form.category_id.default = item.category_id

        # form.process() is run to process the choices and default value
        form.process()

        # The form is provided with the default values after the selectfied
        # has been processed.
        form.name.data = item.name
        form.description.data = item.description
    return render_template('edit_item.html',
                           categories=categories,
                           category=category,
                           item=item,
                           form=form)


@app.route('/delete_item/<int:item_id>', methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    form = ConfirmForm()
    categories = session.query(Category).all()
    item = session.query(Item).filter_by(id=item_id).first()
    if item.user_id != login_session['user_id']:
        flash("You must be the owner to delete this item.", "flash-warning")
        return redirect(url_for('item', item_id=item.id))
    if form.validate_on_submit():
            session.delete(item)
            session.commit()
            flash('Item successfully deleted.', "flash-success")
            return redirect(url_for('index'))
    return render_template('delete_item.html',
                           categories=categories,
                           item=item, form=form)
