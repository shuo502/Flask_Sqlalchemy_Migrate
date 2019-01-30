from app import app
app.run(debug=True,host="0.0.0.0")

# from flask import Flask
# # from admin.views import admin
# # from main.views import main
#
# # app = Flask(__name__)
# # app.register_blueprint(admin, url_prefix='/admin')
# # app.register_blueprint(main, url_prefix='/main')
#
# # print app.url_map
# from flask_sqlalchemy import SQLAlchemy
# from app.routes import apps
# from flask_migrate import Migrate
# from Config import Config
# app=Flask(__name__)
# app.config.from_object(Config)
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
#
# app.register_blueprint(apps,url_prefix='/app')
# app.run()
