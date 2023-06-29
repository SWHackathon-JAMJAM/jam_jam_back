from flask import Blueprint, session, redirect, url_for, render_template, request
import pymysql
from datetime import datetime
# import cv2
#------------------------------------------------------------------------
from db import host,port,user,database, password
#------------------------------------------------------------------------
game = Blueprint("game", __name__, url_prefix="/game")
db = pymysql.connect(host=host, port=port, user=user,password=password, database=database)
cur = db.cursor()

@game.route("/")
def gamestart():
    if not 'id' in session:
        return redirect(url_for('web.login_name'))
    return render_template('game.html')


@game.route("/info")
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

@game.route("/bug_game")
def bug_game():
    return render_template('bug.html')

@game.route("/ant")
def ant():
    return render_template('ant.html')

@game.route("/carrot")
def carrot():
    return render_template('carrot.html')