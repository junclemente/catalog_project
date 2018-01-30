from app import app

from flask import request, render_template, flash, redirect, url_for, g
from flask import session as login_session

from forms import LoginForm

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base

from flask_httpauth import HTTPBasicAuth

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json, random, string
from flask import make_response
import requests

# secret_key = "this is a secret key" # moved to config.py

engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

auth = HTTPBasicAuth()

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/login', methods=['GET', 'POST'])
def show_login():
    error = None
    form = LoginForm()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    if form.validate_on_submit():
        username = form.name.data
        password = form.password.data
        user = session.query(User).filter_by(username=username).first()
        if not user:
            flash('Login unsuccessful.', "flash-warning")
            error = "No username available."
        else:
            if user.verify_password(password):
                token = user.generate_auth_token(600)
                login_session['username'] = user.username
                flash('Login successful.', "flash-success")
                return redirect(url_for('index'))
            else:
                flash('Login unsuccessful.')
    return render_template('login.html', error=error, STATE=state, form=form)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Authorization code upgrade - FAILED.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Confirm access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # Abort if error with access_token info
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify access token is used for intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that access token is valid for app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store access token in the session
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Check if user exists in database
    print login_session['email']
    user_id = getUserId(login_session['email'])
    print user_id
    if not user_id:
        print("New User. Creating record in database.")
        createUser(login_session)
    else:
        print("User exists. Welcome back!")

    login_session['user_id'] = user_id

    print login_session['user_id']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("You are now logged in as %s" % login_session['username'], "flash-success")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        # response = make_response(json.dumps('Current user is not connected.'), 401)
        # response.headers['Content-Type'] = 'application/json'
        flash("Current user is not connected.")
        return redirect(url_for('index'))
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        # response = make_response(json.dumps('Sucessfully disconnected.'), 200)
        # response.headers['Content-Type'] = 'application/json'
        flash("You have been successfully disconnected!", "flash-success")
        return redirect(url_for('index'))


def createUser(login_session):
    newUser = User(username=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserId(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/logout')
def logout():
    del login_session['username']
    flash("You have successfully been logged out.", "flash-success")
    return redirect(url_for('index'))


# For testing purposes only
# @app.route('/forcelogout')
# def forcelogout():
#     del login_session['access_token']
#     del login_session['gplus_id']
#     del login_session['username']
#     del login_session['email']
#     del login_session['picture']
#     del login_session['user_id']
#     flash("Force logout")
#     return redirect(url_for('index'))
