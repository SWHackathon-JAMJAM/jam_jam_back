from flask import Blueprint, session, redirect, url_for, render_template, jsonify, request
import pymysql
from os import listdir, remove, path
from datetime import datetime
# import cv2
#------------------------------------------------------------------------
from db import host,port,user,database, password
#------------------------------------------------------------------------
web = Blueprint("web", __name__, url_prefix="/web")
db = pymysql.connect(host=host, port=port, user=user, password=password, database=database)

@web.route("/")
def index():
    return render_template('web.html')