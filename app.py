from flask import redirect, url_for,jsonify, render_template
from view import app
from datetime import datetime

@app.route("/")
def root():
   return redirect(url_for('web.login_name'))

@app.route('/getServerTime', methods=['GET'])
def get_server_time():
    server_time = datetime.now()
    j = {"ret": server_time}
    print(server_time)
    return jsonify(j)

if __name__ == "__main__":
   app.run(debug=True)
   