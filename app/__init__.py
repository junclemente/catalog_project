from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# Python module was created to better organize code
from app import views, models, restful_api, authenticate, forms


