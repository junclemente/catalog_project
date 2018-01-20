from flask import Flask

app = Flask(__name__)

from app import views, models, restful_api, authenticate


