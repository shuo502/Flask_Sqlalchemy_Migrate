#conding=utf-8
import re, requests,random,datetime
from app import db
from app.models import User,Markbook,Shitou,nbStatus


def r_format(st, a="all"):
    print(st)
    # '''all str int zh'''
    ste=""
    if a == "all":
        ste = re.sub("[\"\'\!\%\[\]\,\@\&\\\\\.<]", "", st)
        pass
    if a == "str":
        ste = ''.join(re.findall(r'[A-Za-z]', st))
        pass
    if a == "int":
        ste = re.sub("\D", "", st)
    if a == "zh":
        ste = re.sub("[\"\'A-Za-z0-9\!\%\[\]\,\。\\\\<\.]", "", st)
    print(ste)
    # st = "hello,world!!%[545]你好234世界。。。"
    return ste

def f_del():
    user = User.query.filter_by(id=1).first()
    db.session.delete(user)
    db.session.commit()
    return 'succeed'

def f_change():
    user = User.query.filter_by(id=2).first()
    user.password = '123567'  # �ύ���ݿ�Ự
    db.session.commit()
    return 'succeed'

def f_insert():
    user = User()
    user.username = 'fuyong'
    user.password = '123'
    db.session.add(user)
    db.session.commit()
    return 'succeed'
def fun(id):
    '''结算'''
    statusid=id
    x1,x2,x3=0,0,0
    a,b,c=0,0,0
    s=Shitou.query.filter_by(nb=statusid).all()
    if s:
        for i in s:
            if str(i.buy)==str(1):
                x1=x1+1
            if str(i.buy)==str(2):
                x2=x2+1
            if str(i.buy)==str(3):
                x3=x3+1
        a,b,c=f_shitou(x1,x2,x3)
    n=x1+x2+x3
    x=[x1,x2,x3]
    if a==b and b==c and a!=0:
        max ="平局"
    else:
        if a>b:
            if a<c:
                max="布"
            else:
                if a!=0:
                    max="石头"
                else:
                    max="无获胜"
        else:
            if b>c:
                max="剪刀"
            else:
                if c != 0:
                    max = "布"
                else:
                    max = "无获胜"

    return str('总计参与{} 石头{},剪刀{},布{}:{} 胜利是：{}'.format(n,a,b,c,x,max))

def re_j(statusid,status_open,status_zhuangtai,status_time,userdata,nowuser):
    t={}
    t['nowuser']=nowuser
    t['userdata']=userdata
    t['statusid'] = str(statusid)
    t['status_open'] = str(status_open)
    t['status_zhuangtai'] = str(status_zhuangtai)
    t['status_time'] = str(status_time)
    t['status_now'] = str(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))
    t['r'] = str(random.random())
    return t

def f_show():
    # shows = Markbook.query.all()
    shows = Markbook.query.order_by("datetimes").all()
    return shows

def f_shitou(a,b,c):
    x1,x2,x3=0,0,0
    if a !=0 and b!=0:x1=b/a
    if c != 0 and b != 0:x2=c/b
    if c != 0 and a != 0:x3=a/c
    return x1,x2,x3

#
# def google(path):
#     s = open(path, 'r', encoding='utf-8').read()
#     r = re.compile('A HREF=\"(.*?)\".*?>(.*?)</')
#     b = r.findall(s)
#     usid = 1
#     for i in b:
#         print(i)
#
#         if len(i[1]) > 1:
#             links = i[0][:499]
#             title = i[1][:499]
#             usid = 1
#             # markbook.create(userid=usid, title=title.encode('utf-8'), links=links.encode('utf-8'), content="")
#
#
# def fx(path):
#     s = open(path, 'r', encoding='utf-8').read()
#     r = re.compile('title\":\"(.*?)\".*?\"uri\":\"(.*?)\"')
#     usid = 1
#     b = r.findall(s)
#     for i in b:
#         if len(i[0]) > 1:
#             links = i[1][:499]
#             title = i[0][:499]
#             # markbook.create(userid=usid, title=title.encode('utf-8'), links=links.encode('utf-8'),content="")
#
#
# # link_all=[]
# # link_title=[]
# # A_url=""
# # A_title=""
# # A_content=""
# #
# # url="https://yangmao.info/pingce/2/"
#
# def s_link(url):
#     # def page
#     re_pageN = re.compile('">(\d+)</a></li><li class="next-page', re.S)
#     re_link_all = re.compile('<a href="(.*?)" title=".*?">(.*?)</a></h2>', re.S)
#     temp_a = requests.get(url).content.decode()
#     print(re_pageN.findall(temp_a))
#     return re_link_all.findall(temp_a)
#
#
# def s_Art(url):
#     temp_a = requests.get(url).content.decode()
#     re_content = re.compile('article-content">(.*?)</article', re.S)
#     return re_content.findall(temp_a)
#     pass
#
#
# def get_title(url):
#     headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#                'Accept - Encoding': 'gzip, deflate',
#                'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
#                'Connection': 'Keep-Alive',
#
#                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
#     # 'Host': 'www.jianshu.com',
#     try:
#         s = requests.get(url, headers=headers)
#         if s.status_code != 200:
#             s = requests.get(url, )
#         y = s.content
#         cookies = s.cookies.get_dict()
#         # print(cookies)
#         # print(y)
#         if len(str(y)) > 300:
#             return "err"
#         # if str(y).find('window.location.href=')>0:
#         #     print(y)
#         #     url = re.compile('.{2}=(.*?), .=(.*?);.*?window.location.href=[\"|\'](.*?)[\"|\']').findall(str(y))
#         #     print(url)
#         #     if len(url)>0:
#         #         u=url[0][2]+str(float(url[0][0])+float(url[0][1]))
#         #         print(u)
#         #         s = requests.get(u, headers=headers)
#         #         y = s.content
#         #         print(y)
#
#         try:
#             scoding = re.compile('charset="(.*?)"').findall(str(y))
#         except:
#             pass
#         if len(scoding) == 0:
#             scoding = s.encoding
#         else:
#             scoding = scoding[0]
#
#         # print(scoding)
#
#         y = y.decode(str(scoding))
#         z = re.compile('title>(.*?)</title')
#         title = z.findall(y)[0]
#         print(title)
#         return str(title)
#     except Exception as E:
#         print(E)
#         return "err"
#
#         # return str(E)
