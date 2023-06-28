from flask import Blueprint, session, redirect, url_for, render_template, jsonify, request
import pymysql
from os import listdir, remove, path
from datetime import datetime
# import cv2
#------------------------------------------------------------------------
from db import host,port,user,database, password
#------------------------------------------------------------------------
game = Blueprint("game", __name__, url_prefix="/game")
db = pymysql.connect(host=host, port=port, user=user,password=password, database=database)

@game.route("/")
def index():
    return render_template('game.html')