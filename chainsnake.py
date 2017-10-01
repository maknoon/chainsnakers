#!~/usr/bin/python3
from flask import Flask, request
import json
import pymysql

app = Flask(__name__)

# ENDPOINT TO FETCH AND POPULATE DB WITH QUIZLET CARDS
@app.route('/setup')
def fetch():
	set_to_fetch = request.args.get('fetch')

	return json.dumps({"message": "fetched the {} set!".format(set_to_fetch)},indent=2)

@app.route('/hello/<u_name>')
def address(u_name):
	return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()
