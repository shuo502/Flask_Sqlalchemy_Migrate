#conding=utf-8

from app import app ,functions,db
from flask import session
import os,re,requests,datetime,json,random
from app.functions import *
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash,make_response
from werkzeug.utils import secure_filename

statusid=int(0)
status_zhuangtai=""
status_open=""
status_time=""
@app.route('/show')
def show_markbook():
    markbooks= Markbook.query.order_by(Markbook.datetimes.desc()).all()
    # markbooks=Markbook.query.order_by(Markbook.RowName.desc()).first()
    return render_template('show.html',markbooks=markbooks)

@app.route('/insert',methods=['POST'])
def insert_markbook():
    markbook = Markbook()
    markbook.title = request.form['title'].encode('utf-8')
    markbook.links = request.form['links'].encode('utf-8')
    if markbook.links:
        print(markbook)
        db.session.add(markbook)
        db.session.commit()
        # flash('New entry was successfully posted')
    return 'success'
    #ɾ


@app.route('/del/<int:ids>')
def del_markbook(ids):
    id=int(ids)
    r=f_del()
    return r


#
@app.route('/change/<int:ids>')
def change_markbook(ids):
    id=int(ids)
    r=f_change()
    return r



@app.route('/cookies')
def cookies():
    ip = request.remote_addr
    name = request.cookies.get('name')  # 获取cookie
    print(request.cookies)
    ua=request.headers.get('User-Agent')
    response=str(ip)+"\n"+str(ua)+str(name)
    if name==None:
        f='登陆/游客'
        response = make_response(response)
        response.set_cookie('name', 'davidszhou')
    # r.set_cookie('name', '', expires=0)#删除
    return response

@app.route('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        ts = User.filter(username=request.form['username'])
        if ts:
            if request.form['password'] != ts[0].password:
                error = 'Invalid password'
                pass
            else:
                print(ts[0])
                session['user'] = ts[0].username
                session['id'] = ts[0].id
                session['is_admin'] = ts[0].is_admin
                session['mail'] =  ts[0].mail
                print("--")
                session['logged_in'] = True
                flash('You were logged in')
                print(session.get('user'))
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
    session['username'] = a
    print(session.get('userkey'))
    s = User()
    s.username=a
    s.password="123456"
    db.session.add(s)
    db.session.flush()
    session['userid'] = s.id
    db.session.commit()
    print("create user id "+str(s.id))
    return redirect(url_for('shitouindex'))

@app.route('/')
def shitouindex():

    if session.get('userid')is None:
        return redirect(url_for('logins'))

        # session['userid'] = a

        # username=int(session)
        # userid = int(session.get['userid'])
    # userid = int(session.get['userid'])
    return render_template('shitou.html')

@app.route('/status')
def status():
    global statusid, status_open,status_zhuangtai,status_time
    t={}
    shows=None
    if statusid !=0 and status_time>datetime.datetime.utcnow()  :
        t['statusid'] = str(statusid)
        t['status_open'] = str(status_open)
        t['status_zhuangtai'] = str(status_zhuangtai)
        t['status_time'] = str(status_time)
        t['status_now'] = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
        t['r'] = str(random.random())
        return json.dumps(t, ensure_ascii=False)

    else:
        try:
            # shows = nbStatus.query.order_by(nbStatus.id).

            shows = nbStatus.query.filter_by(status=True).order_by(nbStatus.id.desc()).first()
            # print(shows)
        except Exception:
            shows=nbStatus()
            shows.status=True
            db.session.add(shows)
            db.session.flush()
            statusid=shows.id
            db.session.commit()
            statusid, status_open,status_zhuangtai,status_time=shows.id,"","尽快选择",shows.datetimes+datetime.timedelta(days=0, seconds=8,  minutes=0, hours=0)
            # return "开奖期数"+str(s.id)
        if shows is None:
            s=nbStatus()
            s.status=True
            db.session.add(s)
            db.session.flush()
            db.session.commit()
            statusid=s.id
            statusid, status_open,status_zhuangtai,status_time=s.id,"","尽快选择",s.datetimes+datetime.timedelta(days=0, seconds=8,  minutes=0, hours=0)
            # return "xx"+str(s.id)
        elif shows.status:
            statusid=shows.id
            t1=shows.datetimes+datetime.timedelta(days=0, seconds=8,  minutes=0, hours=0)
            t2=shows.datetimes+datetime.timedelta(days=0, seconds=10,  minutes=0, hours=0)
            status_time=t1
            if datetime.datetime.utcnow()<t2 and datetime.datetime.utcnow()>t1 :
                status_zhuangtai="结算"
                #结算
                if len(status_open)==0:
                    status_open=fun(statusid)
                    print(status_open)
                    shows.op=str(status_open)
                    db.session.commit()
            elif datetime.datetime.utcnow()>t2  :
                status_zhuangtai="结束"
                #kai
                shows.status=False
                db.session.commit()
                # return "time over"
            else:
                status_zhuangtai="尽快选择"
        # print(shows.datetimes)
    t['statusid']=str(statusid)
    t['status_open']=str(status_open)
    t['status_zhuangtai']=str(status_zhuangtai)
    t['status_time']=str(status_time)
    t['status_now']=str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    t['r']=str(random.random())
    return json.dumps(t,ensure_ascii=False)
    # print((datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=8, weeks=0)).strftime("%Y-%m-%d %H:%M:%S"))
    # return str(shows.id)+str(shows.datetimes)

@app.route('/clean')
def clean():
    session.clear()
    return "clear succeed"


@app.route('/updatebuy/<int:nb>',methods=['POST'])
def updatebuy(nb):
    '''修改 插入'''

    nb=int(nb)
    print(nb)
    b= request.form['buy'].encode('utf-8')
    m= request.form['m'].encode('utf-8')
    print(b,m)
    userid=int(session.get('userid'))
    print(userid)
    #提前2秒结算，停止更新
    if nbStatus.query.filter_by(id=nb).first().status:
        shitou = Shitou.query.filter_by(userid=userid , nb=nb).first()
        if shitou:
            shitou.buy =int(b)
            shitou.m = int(m)
            db.session.commit()
        else:
            shitou = Shitou()
            shitou.nb=nb
            shitou.userid = userid
            shitou.buy = int(b)
            shitou.m = int(m)
            db.session.add(shitou)
            db.session.commit()
        pass
    return "succeed "+str(m)

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