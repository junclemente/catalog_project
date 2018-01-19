from flask import Flask, url_for, render_template
from flask import jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Category, Item


app = Flask(__name__)


engine = create_engine('sqlite:///catalogProject.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def index():
    # return "<h1>Hello World!</h1>"
    return render_template('index.html')


@app.route('/categoryJSON')
@app.route('/catagoryjson')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [c.serialize for c in categories])


@app.route('/itemJSON/<int:id>')
@app.route('/itemjson/<int:id>')
def itemJSON(id):
    items = session.query(Item).filter_by(category_id=id).all()
    return jsonify(items = [i.serialize for i in items])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)


