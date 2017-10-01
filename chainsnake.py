#!~/usr/bin/python3
from flask import Flask, request
import pymysql
import json
import chainsnakedb

app = Flask(__name__)

@app.route('/setup')
def fetch():
    set_to_fetch = request.args.get('fetch')
    chaindb = chainsnakedb.ChainsDb()
    response = chaindb.get_questions_given_question("The chairman of China")
    response["topic"] = set_to_fetch
    response["description"] = "Information about important figures in political history of China"
    return json.dumps(response)

@app.route('/hello/<u_name>')
def address(u_name):
    return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/getnext')
def question():
    key = request.args.get('key')
    chaindb = chainsnakedb.ChainsDb()
    response = chaindb.get_questions_given_question(key)
    return json.dumps(response)

@app.route('/question')
def word():
    key = request.args.get('key')
    chaindb = chainsnakedb.ChainsDb()
    response = chaindb.get_keyword_given_question(key)
    return json.dumps(response)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()
