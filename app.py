from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

web_app = Flask(__name__)

database_url_default = 'sqlite:///default.db'
web_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', database_url_default)
web_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(web_app)

from routes import *

if __name__ == '__main__':
    web_app.run(debug=True, port=5000)