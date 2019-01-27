#conding=utf-8
from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(128),nullable=False)
    datetimes = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Markbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(256),default="")
    links =  db.Column(db.String(128),nullable=False)
    datetimes = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    def __repr__(self):
        return '<Markbook {}>'.format(self.links)

class Shitou(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nb=db.Column(db.Integer,nullable=False)
    userid= db.Column(db.Integer, db.ForeignKey('user.id'))
    buy=db.Column(db.Integer,nullable=False)
    m=db.Column(db.Integer,nullable=False)
    k=db.Column(db.Integer,nullable=False)
    def __repr__(self):
        return '<Shitou {}>'.format(self.buy)
class nbStatus(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    op=db.Column(db.String(128),default="")
    status=db.Column(db.Boolean,default=True)
    datetimes = db.Column(db.DateTime, index=True, default=datetime.utcnow)
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