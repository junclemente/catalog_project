from app import app

from flask import request, render_template, flash, redirect, url_for, g
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base

from flask_httpauth import HTTPBasicAuth

secret_key = "this is a secret key"

engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()

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
                login_session['username'] = user.username
                token = user.generate_auth_token
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token
    return jsonify({'token': token.decode('ascii')})


@app.route('/logout')
def logout():
    del login_session['username']
    flash("You have successfully been logged out.")
    return redirect(url_for('index'))
