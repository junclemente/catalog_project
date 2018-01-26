from app import app

from flask import request, render_template, flash, redirect, url_for, g
from flask import session as login_session

from forms import LoginForm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base

from flask_httpauth import HTTPBasicAuth
import json

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
from flask import make_response
import requests

# secret_key = "this is a secret key"

engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

@auth.verify_password
def verify_password(username_or_token, password):
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/login/<provider>', methods=['POST'])
def oauth_login(provider):
    # Parse auth code
    auth_code = request.json.get('auth_code')
    if provider == 'google':
        # Exchange auth_code for token
        try:
            # Upgrade auth code into credentials object
            oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(auth_code)
        except FlowExchangeError:
            response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        # Check that access token is valid
        access_token = credentials.access_token
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1])
        # Abort if error in access token info
        if result.get('error') is not None:
            reponse = make_response(json.dumps(result.get('error')), 500)
            response.headers['Content-Type'] = 'application/json'

        # Get user info
        h = httplib2.Http()
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt':'json'}
        answer = requests.get(userinfo_url, params=params)

        data = answer.json()

        name = data['name']
        picture = data['picture']
        email = data['email']

        # Add user to database if does not exist
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(username = name, picture=picture, email=email)
            session.add(user)
            session.commit()

        # Create token
        token = user.generate_auth_token(600)

        # Send token back to client
        return jsonify({'token': token.decode('ascii')})
    else:
        return "Unrecognized Provider"



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        user = session.query(User).filter_by(username=username).first()
        if not user:
            flash('Login unsuccessful.')
            error = "No username available."
        else:
            if user.verify_password(password):
                token = user.generate_auth_token(600)
                login_session['username'] = user.username
                flash('Login successful.')
                return redirect(url_for('index'))
            else:
                flash('Login unsuccessful.')
    return render_template('login.html', error=error, form=form)


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
