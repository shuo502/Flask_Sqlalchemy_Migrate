#conding=utf-8
from datetime import datetime
from app import db
import json
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,comment="姓名")
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128),nullable=False)
    datetimes = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    # def __init__(self, a1, a2):
    #     self.a1 = a1
    #     self.a2 = a2
    # def to_json(self):
    #     json_data = {
    #         'id': self.id,
    #         'a1': self.a1,
    #         'a2': self.a2,
    #         'a3': self.a3,
    #         'a4': self.a4,
    #         'a5': self.a5
    #     }
    #     return json.dumps(json_data,cls=DateEncoder)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Markbook(db.Model):
    __tablename__ = 'Markbook'
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(256),default="")
    links =  db.Column(db.String(128),nullable=False)
    datetimes = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __repr__(self):
        return '<Markbook {}>'.format(self.links)

class Shitou(db.Model):
    __tablename__ = 'shitou'
    id = db.Column(db.Integer, primary_key=True)
    nb=db.Column(db.Integer,nullable=False)
    userid= db.Column(db.Integer, db.ForeignKey('user.id'))
    buy=db.Column(db.Integer,nullable=False)
    m=db.Column(db.Integer,nullable=False)
    k=db.Column(db.Integer,nullable=True,comment="开了")
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __repr__(self):
        return '<Shitou {}>'.format(self.buy)

class nbStatus(db.Model):
    __tablename__ = 'nbstatus'
    id= db.Column(db.Integer, primary_key=True)
    op=db.Column(db.String(128),default="")
    status=db.Column(db.Boolean,default=True)
    datetimes = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    __table_args__ = {
        "mysql_charset": "utf8"
    }
    def __repr__(self):
        return '<nbstatus {} {}>'.format(self.id,self.status)

if __name__=='__main__':
    a=datetime.now()
    print(a)
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

# class User(db.Model):
#     id=db.Column(db.Integer, primary_key=True)
#     username =db.Column(db.String(64), index=True, unique=True)
#     password=  db.Column(db.String(128),nullable=False)
#     def __repr__(self):
#         return '<User {}>'.format(self.username)

# class Markbook(db.Model):
#     userid = db.Column(User, related_name='tweets')
#     title=db.Column( null=True,max_length=500)
#     content = db.Column(null=True)
#     message = db.Column(null=True)
#     links = db.Column(null=True ,max_length=500)
#     created_date = db.Column(default=datetime.datetime.now)
#     is_published = db.Column(default=True)
#     def __repr__(self):
#         return '<Markbook {}>'.format(self.links)

    # db.session.add(user)
    # db.session.commit()