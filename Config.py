#conding=utf-8
import os
from key import key
basedir = os.path.abspath(os.path.dirname(__file__))
# o=("mysql+pymysql://root:s@ts:3306/t1?charset=utf8",echo=True,encoding='utf-8',convert_unicode=True)

mysql_config='mysql+pymysql://{}:{}@{}:3306/{}?charset=utf8'.format(key[0],key[1],key[2],key[3])
sqlite_config='sqlite:///' + os.path.join(basedir, 'app.db')
# print(mysql_config)
class Config(object):
    SECRET_KEY='development key',
    # ...
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or   sqlite_config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or   mysql_config
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
