from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




app=Flask(__name__)
app.config['SECRET_KEY']='50073040194fffe20e0f8b08a331d41a'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
loginmanager=LoginManager(app)
loginmanager.login_view='login'
loginmanager.login_message_category='info'
from flask_blog import routes
