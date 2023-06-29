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

@menu.route("/info")
def info():
    mb_id = session['id']
    sql = 'SELECT mb_id FROM game WHERE mb_id = %s'
    cur.execute(sql,(mb_id))
    res = cur.execute(sql, (mb_id))
    if res == 0:
        return redirect(url_for('web.login_name'))
    sql = 'SELECT level, charter,last_play FROM game WHERE mb_id = %s'
    res = cur.execute(sql, (mb_id))
    if res == 0:
        return redirect(url_for('web.login_name'))
    
    level, charter, last_play = cur.fetchall()[0]
    return render_template('info.html', id = mb_id, level = level, last_play = last_play)

@menu.route("/level1")
def level1():
    # return redirect(url_for('game.index'))
    return render_template('level1.html')

@menu.route("/level2")
def level2():
    return render_template('level2.html')

@menu.route("/level3")
def level3():
    return render_template('level3.html')