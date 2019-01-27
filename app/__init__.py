#conding=utf-8
from flask import Flask,render_template
from Config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# app = Flask(__name__,)
app=Flask(__name__,static_folder="template_folder='../templates",)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models,functions



# @app.route('/shohw')
# def show_markbookh():
#     # r=f_show()
#     return render_template('show.html')

#
# from flask import Flask
# from Config import Config
# from flask_sqlalchemy import SQLAlchemy
#
# #
# from flask import Blueprint, render_template
# app = Blueprint('main', __name__, template_folder='sss')
#
# # app = Flask('app',__name__,template_folder='templates')
#
#
# from app import routes, models,functions