# conding=utf-8

from app import app, functions, db
from flask import session
import os, re, requests, datetime, json, random,time
from app.functions import *
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response
from werkzeug.utils import secure_filename

statusid = int(0)
status_zhuangtai = ""
status_open = ""
status_time = ""
userdata = []
nowuser = []
nowuser_dict = {}


@app.route('/show')
def show_markbook():
    markbooks = Markbook.query.order_by(Markbook.datetimes.desc()).all()
    # markbooks=Markbook.query.order_by(Markbook.RowName.desc()).first()
    return render_template('show.html', markbooks=markbooks)


@app.route('/insert', methods=['POST'])
def insert_markbook():
    markbook = Markbook()
    markbook.title = r_format(request.form['title'].encode('utf-8'))
    markbook.links = request.form['links'].encode('utf-8')
    if markbook.links:
        # print(markbook)
        db.session.add(markbook)
        db.session.commit()
        # flash('New entry was successfully posted')
    return 'success'
    # ɾ


@app.route('/del/<int:ids>')
def del_markbook(ids):
    id = int(ids)
    r = f_del()
    return r


#
@app.route('/change/<int:ids>')
def change_markbook(ids):
    id = int(ids)
    r = f_change()
    return r


@app.route('/cookies')
def cookies():
    ip = request.remote_addr
    name = request.cookies.get('name')  # 获取cookie
    # print(request.cookies)
    ua = request.headers.get('User-Agent')
    response = str(ip) + "\n" + str(ua) + str(name)
    if name == None:
        f = '登陆/游客'
        response = make_response(response)
        response.set_cookie('name', 'davidszhou')
    # r.set_cookie('name', '', expires=0)#删除
    return response


@app.route('/login')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ts = User.filter(username=r_format(request.form['username']))
        if ts:
            if request.form['password'] != ts[0].password:
                error = 'Invalid password'
                pass
            else:
                # print(ts[0])
                session['user'] = ts[0].username
                session['id'] = ts[0].id
                session['is_admin'] = ts[0].is_admin
                session['mail'] = ts[0].mail
                # print("--")
                session['logged_in'] = True
                flash('You were logged in')
                # print(session.get('user'))
                return redirect(url_for('show_entries'))
        else:
            error = 'Invalid username'
    return render_template('login.html', error=error)


#
# def login():
#     # us=request.get_data()
#     us= request.args['login']
#     name = request.cookies.get('name')  # 获取cookie
#     if name==None:
#         if us=="":
#             return url_for(login)
#         elif us=="":
#             response = make_response()
#             response.set_cookie('name', 'davidszhou')
#             pass
#
@app.route('/logins')
def logins():
    a = int(random.randint(100000, 999999))
    session['username'] = str(a)
    # print(session.get('userkey'))
    s = User()
    s.username = str(a)
    s.password = "123456"
    db.session.add(s)
    db.session.flush()
    session['userid'] = s.id
    db.session.commit()
    # print("create user id " + str(s.id))
    return redirect(url_for('shitouindex'))
    
@app.route('/wx_login')
def wx_login():
    a = int(random.randint(100000, 999999))
    session['username'] = str(a)
    # print(session.get('userkey'))
    s = User()
    s.username = str(a)
    s.password = "123456"
    db.session.add(s)
    db.session.flush()

    # print("create user id " + str(s.id))
    return "login succeed"



@app.route('/')
def shitouindex():
    if session.get('userid') is None:

        return redirect(url_for('logins'))

        # session['userid'] = a

        # username=int(session)
        # userid = int(session.get['userid'])
    # userid = int(session.get['userid'])
    return render_template('shitou.html')


@app.route('/status_user/<int:istatusid>')
def status_user(istatusid):
    istatusid = int(istatusid)
    # username = db.session.query(User.username).filter(User.id == Shitou.userid, Shitou.nb == int(istatusid)).order_by(
    #     Shitou.id.desc()).all()
    username = db.session.query(User.id,User.username,Shitou.buy).filter(User.id == Shitou.userid, Shitou.nb == int(istatusid)).order_by(
        Shitou.id.desc()).all()
    s = {"userdata": username}
    # s["aa"]=['a','b','c']
    # alluser = db.session.query(Shitou.userid).filter_by(nb=int(statusid)).order_by(Shitou.id.desc()).all()
    # print(username)
    return json.dumps(s, ensure_ascii=False)


# print(session.query(User, Address).filter(User.id == Address.user_id).all())
@app.route("/changename", methods=['POST'])
def changename():
    r=r_format(request.form["username"]).encode("utf-8")

    if r==session.get('username'):return "zzzz"
    # print (r)
    userid=session.get('userid')
    t=User.query.filter_by(id=userid).first()
    # r=r.replace(".").replace("<").replace("'").replace("/").replace("\\").replace("\"").replace("&")
    t.username=r
    db.session.commit()

    nowuser.remove(session.get('username'))
    del nowuser_dict[session.get('username')]

    session['username']=r.decode()

    global userdata,statusid




    userdata = db.session.query(User.id ,User.username).filter(User.id == Shitou.userid, Shitou.nb == int(statusid)).order_by(
            Shitou.id.desc()).all()
    return "successd"




@app.route('/status')
def status():

    userbuy=""
    t1x = 15
    t2x = 25

    global statusid, status_open, status_zhuangtai, status_time, userdata,nowuser,nowuser_dict

    usernames=str(session.get("username"))
    t_time = int(time.time())

    nowuser_dict[usernames] = t_time
    if usernames:
        if usernames not in nowuser:
            nowuser.append(usernames)

    if len(nowuser)>0:
        for i in nowuser:
            if int(nowuser_dict[i])+10 < int(t_time):
                s=str(i)
                nowuser.remove(s)
                del nowuser_dict[s]
    t = {}
    shows = None
    # print(statusid, status_open, status_zhuangtai, status_time)
    # print("----")
    if statusid != 0 and status_time > datetime.datetime.utcnow():
        # t['userdata']==db.session.query(User.username).filter(User.id==Shitou.userid , Shitou.nb==int(istatusid)).order_by(Shitou.id.desc()).all()
        # print("~1")

        return json.dumps(re_j(statusid, status_open, status_zhuangtai, status_time, userdata,nowuser), ensure_ascii=False)
    else:
        try:
            # print("~2")
            # shows = nbStatus.query.order_by(nbStatus.id).
            shows = nbStatus.query.filter_by(status=True).order_by(nbStatus.id.desc()).first()
            # print(shows)
        except Exception:
            # print("~3")
            shows = nbStatus()
            shows.status = True
            db.session.add(shows)
            db.session.flush()
            statusid = shows.id
            db.session.commit()
            statusid, status_open, status_zhuangtai, status_time, userdata = shows.id, "", "尽快选择", shows.datetimes + datetime.timedelta(
                days=0, seconds=int(t1x), minutes=0, hours=0), []
            # return "开奖期数"+str(s.id)
        if shows is None:
            # print("~4")
            s = nbStatus()
            s.status = True
            db.session.add(s)
            db.session.flush()
            db.session.commit()
            statusid = s.id
            statusid, status_open, status_zhuangtai, status_time, userdata = s.id, "", "尽快选择", s.datetimes + datetime.timedelta(
                days=0, seconds=int(t1x), minutes=0, hours=0), []
            # return "xx"+str(s.id)
        elif shows.status:
            # print("~5")
            statusid = shows.id
            t1 = shows.datetimes + datetime.timedelta(days=0, seconds=int(t1x), minutes=0, hours=0)
            t2 = shows.datetimes + datetime.timedelta(days=0, seconds=int(t2x), minutes=0, hours=0)
            status_time = t1
            if datetime.datetime.utcnow() < t2 and datetime.datetime.utcnow() > t1:
                # print("~6")
                if status_zhuangtai == "结算":
                    # print("~7")
                    return json.dumps(re_j(statusid, status_open, status_zhuangtai, status_time, userdata,nowuser),
                                      ensure_ascii=False)
                else:
                    # print("~8")
                    status_zhuangtai = "结算"
                    userdata = db.session.query(User.id,User.username,Shitou.buy).filter(User.id == Shitou.userid, Shitou.nb == int(statusid)).order_by(
            Shitou.id.desc()).all()
                    if len(status_open) == 0:
                        status_open = fun(statusid)
                        # print(status_open)
                        shows.op = str(status_open)
                        db.session.commit()
                    # print("~8.1")
                    return json.dumps(re_j(statusid, status_open, status_zhuangtai, status_time, userdata,nowuser),
                                      ensure_ascii=False)

            elif datetime.datetime.utcnow() > t2:
                # print("~9")
                if status_zhuangtai == "结束":
                    # print("~10")

                    return json.dumps(re_j(statusid, status_open, status_zhuangtai, status_time, userdata,nowuser),
                                      ensure_ascii=False)
                else:
                    status_zhuangtai = "结算"
                    userdata = db.session.query(User.id,User.username,Shitou.buy).filter(User.id == Shitou.userid, Shitou.nb == int(statusid)).order_by(
            Shitou.id.desc()).all()
                    # print("~11")
                    # kai
                    shows.status = False
                    db.session.commit()

                    s = nbStatus()
                    s.status = True
                    db.session.add(s)
                    db.session.flush()
                    db.session.commit()
                    statusid = s.id
                    statusid, status_open, status_zhuangtai, status_time, userdata = s.id, "", "尽快选择", s.datetimes + datetime.timedelta(
                        days=0, seconds=int(t1x), minutes=0, hours=0), []

                    return json.dumps(re_j(statusid, status_open, status_zhuangtai, status_time, userdata,nowuser),
                                      ensure_ascii=False)
                # return "time over"
            else:
                status_zhuangtai = "尽快选择"
        # print(shows.datetimes)
    return json.dumps(re_j(statusid, status_open, status_zhuangtai, status_time,userdata,nowuser), ensure_ascii=False)
    # print((datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=8, weeks=0)).strftime("%Y-%m-%d %H:%M:%S"))
    # return str(shows.id)+str(shows.datetimes)


@app.route('/clean')
def clean():
    session.clear()
    return "clear succeed"


@app.route('/updatebuy/<int:nb>', methods=['POST'])
def updatebuy(nb):
    '''修改 插入'''
    global userdata
    nb = int(nb)
    # print(nb)
    # print(request.form)
    b = r_format(request.form['buy']).encode('utf-8')
    m = r_format(request.form['m']).encode('utf-8')
    if status_zhuangtai == "": return "结算 "
    # print(b, m)
    userid = int(session.get('userid'))
    # print(userid)
    # 提前2秒结算，停止更新
    if nbStatus.query.filter_by(id=nb).first().status:
        shitou = Shitou.query.filter_by(userid=userid, nb=nb).first()
        if shitou:
            shitou.buy = int(b)
            shitou.m = int(m)
            db.session.commit()
        else:
            shitou = Shitou()
            shitou.nb = nb
            shitou.userid = userid
            shitou.buy = int(b)
            shitou.m = int(m)
            db.session.add(shitou)
            db.session.commit()
        pass
        userdata = db.session.query(User.id,User.username).filter(User.id == Shitou.userid, Shitou.nb == int(nb)).order_by(
            Shitou.id.desc()).all()
    return "succeed " + str(m)

# @app.route('/')
# def show_entries():
#     entries = db.markbook.filter(is_open=True).order_by(db.markbook.id.desc())
#     return render_template('show_entries.html', entries=entries)
#
# @app.route('/bookmark/<int:id>')
# def re_302(id):
#     id=int(id)
#     entries = markbook.filter(markbook.id == id)[0]
#     #print(entries.links)
#     link=entries.links
#     return redirect(link)
#     # return '',302,{'Location' ,'http://xxx.xx'}
#
# @app.route('/s')
# def mk_s():
#     print("sssssss")
#
# @app.route('/add', methods=['POST'])
# def add_entry():
#     if not session.get('logged_in'):
#         abort(401)
#     title = request.form['title']
#     links = request.form['links']
#     content=request.form['content']
#     if not title:title=get_title(links)
#     markbook.create(userid=session.get('id') , title=title.encode('utf-8'),links= links.encode('utf-8'),content=content.encode('utf-8'))
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
# @app.route('/upload', methods=['POST', 'GET'])
# def upload():
#     if request.method == 'POST':
#         f = request.files['file']
#         basepath = os.path.dirname(__file__)  # ��ǰ�ļ�����·��
#         print(f.filename)
#         upload_path = os.path.join(basepath, 'static\\uploads',secure_filename(f.filename))  #ע�⣺û�е��ļ���һ��Ҫ�ȴ�������Ȼ����ʾû�и�·��
#         print(upload_path)
#         f.save(upload_path)
#         if 'json'in upload_path:fx(upload_path)
#         if 'html'in upload_path:google(upload_path)
#         return redirect(url_for('show_entries'))
#     return '''
#     <!doctype html>
#     <title>Upload new File</title>
#     <h1>Upload new File</h1>
#     <form method=post enctype=multipart/form-data>
#       <input type=file name=file>
#       <input type=submit value=Upload>
#     </form>
#     '''
#
#
# @app.route('/addus' ,methods=['GET', 'POST'])
# def addus():
#     if not session.get('logged_in'):
#         abort(401)
#     if session.get('is_admin')==False:
#         abort(401)
#     return render_template('addus.html')
#
# @app.route('/adduser', methods=['POST'])
# def add_user():
#     if not session.get('logged_in'):
#         abort(401)
#     if session.get('is_admin')==False:
#         abort(401)
#     User.create(username=request.form['user'], password=request.form['password'],mail=request.form['mail'])
#     flash('New entry was successfully posted')
#     return redirect(url_for('show_entries'))
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         ts = User.filter(username=request.form['username'])
#         if ts:
#             if request.form['password'] != ts[0].password:
#                 error = 'Invalid password'
#                 pass
#             else:
#                 print(ts[0])
#                 session['user'] = ts[0].username
#                 session['id'] = ts[0].id
#                 session['is_admin'] = ts[0].is_admin
#                 session['mail'] =  ts[0].mail
#                 print("--")
#                 session['logged_in'] = True
#                 flash('You were logged in')
#                 print(session.get('user'))
#                 return redirect(url_for('show_entries'))
#         else:
#             error = 'Invalid username'
#     return render_template('login.html', error=error)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     session.pop('user', None)
#     session.pop('id', None)
#     session.pop('is_admin', None)
#     session.pop('mail', None)
#     flash('You were logged out')
#     return redirect(url_for('show_entries'))
#
# @app.route('/up_date/<int:id>')
# def up_date(id):
#     if not session.get('logged_in'):
#
#         abort(401)
#
#     id=int(id)
#     entries = markbook.filter(markbook.id == id)[0]
#     #print(entries.links)
#     title=str(get_title(entries.links))
#     #print(title)
#     if title=="err":return redirect(url_for('show_entries'))
#     nrows = (markbook.update(title=title.encode('utf-8')).where(markbook.id==id).execute())
#     #print(nrows)
#     return redirect(url_for('show_entries'))
#
# @app.route('/links_edit/<id>')
# def links_edit(id):
#     if not session.get('logged_in'):
#         abort(401)
#     id = int(id)
#     print(id)
#     return redirect(url_for('show_entries'))
#
