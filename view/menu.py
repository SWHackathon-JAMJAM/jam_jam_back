from flask import Blueprint, session, redirect, url_for, render_template, request
import pymysql
from datetime import datetime
# import cv2
#------------------------------------------------------------------------
from db import host,port,user,database, password
#------------------------------------------------------------------------
menu = Blueprint("menu", __name__, url_prefix="/menu")
db = pymysql.connect(host=host, port=port, user=user,password=password, database=database)
cur = db.cursor()


@menu.route("/")
def gamestart():
    if not 'id' in session:
        return redirect(url_for('web.login_name'))
    return render_template('game.html')


@menu.route("gameselect")
def gameselect():
    return render_template('selectLevel.html')

@menu.route("handselect")
def handselect():
    return render_template('selectHand.html')

@menu.route("/info")
def info():
    mb_id = session['id']
    sql = 'SELECT mb_id FROM game WHERE mb_id = %s'
    cur.execute(sql,(mb_id))
    res = cur.execute(sql, (mb_id))
    if res == 0:
        return redirect(url_for('web.login_name'))
    sql = 'SELECT mb_exp FROM game WHERE mb_id = %s'
    cur.execute(sql, (mb_id))
    if res == 0:
        return redirect(url_for('web.login_name'))
    
    res = cur.fetchall()[0]
    if (res[0] is None):
        exp_tmp = 1
    else:
        exp_tmp = res[0]

    if exp_tmp>=1 and exp_tmp < 5: 
        level = 2
    elif exp_tmp >= 5 and exp_tmp < 15:
        level = 3
    elif exp_tmp >= 15 and exp_tmp < 25:
        level = 4
    elif exp_tmp >= 25 and exp_tmp < 35:
        level = 5
    elif exp_tmp >= 35 and exp_tmp < 45:
        level = 6
    elif exp_tmp >= 45 and exp_tmp < 60:
        level = 7
    elif exp_tmp >= 60 and exp_tmp < 75:
        level = 8
    elif exp_tmp >= 75 and exp_tmp < 90:
        level = 9
    elif exp_tmp >= 90:
        level = 10
    else:
        level = 1
    if level ==1:
        level_info = 0     
    elif level>=2 and level<= 5:
        level_info = 1
    elif level>=6 and level<= 8:
        level_info = 2
    elif level>8:
        level_info = 3   
    return render_template('info.html', id = mb_id, exp = res[0], level = level, level_info = level_info)

@menu.route("/level1")
def level1():
    return render_template('level1.html')

@menu.route("/level2")
def level2():
    return render_template('level2.html')

@menu.route("/level3")
def level3():
    return render_template('level3.html')