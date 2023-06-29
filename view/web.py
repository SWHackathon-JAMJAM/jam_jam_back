from flask import Blueprint, session, redirect, url_for, render_template,  request
import pymysql
#------------------------------------------------------------------------
from db import host,port,user,database, password
#------------------------------------------------------------------------
web = Blueprint("web", __name__, url_prefix="/web")
db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)
cur = db.cursor()


@web.route("/admin")
def admin():
    return render_template('admin.html')

@web.route("/login_name")
def login_name():
    session.clear()
    return render_template('index.html')

@web.route("/login_name_back", methods=['POST'])
def login_name_back():
    # id 정보 받아오기
    inp_id = request.form['id']

    # database에 id 존재하는지 확인
    sql = "SELECT EXISTS (SELECT mb_id FROM member WHERE mb_id = %s LIMIT 1) AS SUCCESS;"
    cur.execute(sql, (inp_id))
    res = cur.fetchall()[0]
    if(res[0] == 0):
        return redirect(url_for('web.login_name'))
    
    session['id'] = inp_id
    return redirect(url_for('web.login_pw'))
    
@web.route("/login_pw")
def login_pw():
    return render_template('pw.html')

@web.route("/login_pw_back", methods = ['POST'])
def login_pw_back():
    mb_pw = request.form['pw']
    mb_id = session['id']
    # id와 pw가 일치하는지 확인
    sql = "SELECT mb_pw FROM member WHERE mb_id = %s"
    cur.execute(sql,(mb_id))
    tmp_pw = cur.fetchall()[0]
    if mb_id == 'admin' and mb_pw=='1234':
        return redirect(url_for('web.admin'))
    if str(tmp_pw[0]) == mb_pw:
        session['id'] = mb_id
        return redirect(url_for('menu.gamestart'))
    else:
        return redirect(url_for('web.login_name'))
