import flask
import os
from flask import jsonify
import random
import time
import sqlite3
import sys
import hashlib

app = flask.Flask(__name__)
port = int(os.getenv("PORT", 9099))

t = round(time.time())

# Document Create Page
@app.route('/new')
def new():
	id = ''.join(random.choice('123456789abcdefghijklmnpqrstuvwxyz') for i in range(5))
	conn = sqlite3.connect('data.db')
	conn.execute(f"INSERT INTO DATA (ID, TIMESTAMP, CONTENT, UPDATE_TIME) VALUES ('{id}', {round(time.time())}, '', {round(time.time())});")
	conn.commit()
	conn.close()
	h = "{} 3h43c432u47324832x4".format(id).encode('utf-8')
	hash_value = hashlib.sha256(h).hexdigest()
	response = flask.make_response(flask.redirect('/'+str(id)))
	response.set_cookie('hash', hash_value, path = "/"+str(id))
	return response

@app.route('/update', methods = ['POST'])
def update():
    data = flask.request.form['data']
    id = flask.request.form['id']
    conn = sqlite3.connect('data.db')
    conn.execute(f"UPDATE DATA set CONTENT = '{data}', UPDATE_TIME = {round(time.time())} where ID = '{id}'")
    conn.commit()
    conn.close()
    return jsonify(result = "Success")

# Document View Page
@app.route('/<id>')
def view(id):
	h = "{} 3h43c432u47324832x4".format(id).encode('utf-8')
	hash_value = hashlib.sha256(h).hexdigest()
	if flask.request.cookies.get('hash') == hash_value:
	    conn = sqlite3.connect('data.db')
	    cur = conn.cursor()
	    cur.execute(f"SELECT CONTENT FROM DATA where ID = '{id}'")
	    result = cur.fetchone()
	    conn.close()
	    if not result:
		    result = ""
	    return flask.render_template('interactive.html', id = id, data = result[0])
	else:
		return flask.render_template('view.html', id = id)

@app.route('/doc/<id>', methods = ['POST'])
def document_view(id):
    global t
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute(f"SELECT CONTENT, UPDATE_TIME FROM DATA where ID = '{id}'")
    result = cur.fetchone()
    conn.close()
    if result[1] > t:
	    t = result[1]
	    return jsonify(result = result[0])
    else:
	    return jsonify(result = "No Update"), 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
