from app import app

from flask import Flask, url_for, render_template, request, g
from flask import jsonify, flash, redirect

from flask.ext.httpauth import HTTPBasicAuth

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item


# app = Flask(__name__)
app.secret_key = 'secret key'
auth = HTTPBasicAuth()

engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).first()
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/')
@app.route('/index')
def index():
    # return "<h1>Hello World!</h1>"
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if not user:
            flash('Login unsuccessful.')
            error = "No username available"
        elif user:
            if user.verify_password(password):
                token = user.generate_auth_token(600)
                flash('Login successful.')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token
    return jsonify({'token': token.decode('ascii')})


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


# if __name__ == '__main__':
#     app.debug = True
#     app.run(host='0.0.0.0', port=8000)


