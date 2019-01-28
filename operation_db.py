#conding=utf-8
from app.models import User
from app import db

def select_user():
    markbooks= User.query.order_by(User.id.desc()).all()
    markbooks= User.query.order_by(User.id.desc()).limit(10).all()
    page_size,page_index=1 ,10
    db.session.query(User.name).filter(User.email.like('%' + email + '%')).limit(page_size).offset( (page_index - 1) * page_size)
    # 查询所有用户
    users_list = User.query.all()

    # 查询用户名称为 fuyong 的第一个用户, 并返回用户实例, 因为之前定义数据库的时候定义用户名称唯一, 所以数据库中用户名称为 test 的应该只有一个.
    user = User.query.filter_by(username='fuyong').first()
    # or
    user = User.query.filter(User.username == 'fuyong').first()

    # 模糊查询, 查找用户名以abc 结尾的所有用户
    users_list = User.query.filter(User.username.endsWith('g')).all()

    # 查询用户名不是 fuyong 的第一个用户
    user = User.query.filter(User.username != 'fuyong').first()


def update_user():
    # 获取用户对象
    user = User.query.filter_by(id=2).first()

    # 修改用户
    user.password = '123567'

    # 提交数据库会话
    db.session.commit()




def delete_user():
    # 获取用户对象
    user = User.query.filter_by(id=1).first()

    # 删除用户
    db.session.delete(user)

    # 提交数据库会话
    db.session.commit()


def create_user():
    # 创建一个新用户对象
    user = User()
    user.username = 'fuyong'
    user.password = '123'

    # 将新创建的用户添加到数据库会话中
    db.session.add(user)
    # 将数据库会话中的变动提交到数据库中, 记住, 如果不 commit, 数据库中是没有变化的.
    db.session.commit()



"""
    类型名                  Python类型                     说　　明
Integer                   int 普通整数，              一般是 32 位
SmallInteger          int 取值范围小的整数   一般是 16 位
BigInteger              int 或 long                    不限制精度的整数
Float                      float                              浮点数
Numeric                decimal.Decimal           定点数
String                    str                                 变长字符串
Text                       str               变长字符串，对较长或不限长度的字符串做了优化
Unicode                 unicode                    变长 Unicode 字符串
UnicodeText         unicode                对较长或不限长度的字符串做了优化
Boolean                 bool                           布尔值
Date                    datetime.date               日期
Time                    datetime.time               时间
DateTime           datetime.datetime          日期和时间
Interval                datetime.timedelta          时间间隔
Enum                   str                                   一 组字符串
PickleType           任何 Python 对象           自动使用 Pickle 序列化
LargeBinary         str                                   二进制文件


primary_key         如果设为 True，这列就是表的主键
unique                  如果设为 True，这列不允许出现重复的值
index                   如果设为 True，为这列创建索引，提升查询效率
nullable                如果设为 True，这列允许使用空值；如果设为 False，这列不允许使用空值
default                 为这列定义默认值
doc                      字段说明

"""

'''

上面说了设置与获取session
那么如何删除session呢？
可以直接使用session.pop('key',None) 即：
session.pop('name',None)
如果要删除session中所有数据使用：clear()即：
session.clear()

'''
