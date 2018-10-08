

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import os

from config import app_config


#webapp = Flask(__name__)


db = SQLAlchemy()


config_name = os.getenv('FLASK_CONFIG')
webapp = Flask(__name__, instance_relative_config=True)
webapp.config.from_object(app_config[config_name])
webapp.config.from_pyfile('config.py')
db.init_app(webapp)
migrate = Migrate(webapp, db)


from app import models

from app import main
from app import login
from app import user




