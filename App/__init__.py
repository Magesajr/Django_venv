from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy 
from .config import config
from flask_mail import Mail
import os
from flask_moment import Moment
from flask_login import LoginManager


bootstrap=Bootstrap5()
mail=Mail()
db=SQLAlchemy()
manager=LoginManager()
manager.login_view='tickets.home'
moment=Moment()

def create_app(config_option):
    app=Flask('__name__',template_folder='App/templates',static_folder='App/static')
    app.config.from_object(config[config_option])
    config[config_option].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    manager.init_app(app)

    from .tikets import tickets
    from .Admin import admin

    app.register_blueprint(tickets,url_prefix='/tikets')
    app.register_blueprint(admin,url_prefix='/Admin')
    
    return app