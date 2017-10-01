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
    response = chaindb.get_questions_given_keyword('cell barrier')
    response["topic"] = set_to_fetch
    response["description"] = "Animals and natural reproduction"
    return json.dumps(response)

@app.route('/hello/<u_name>')
def address(u_name):
    return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/word')
def question():
    key = request.args.get('key')
    chaindb = chainsnakedb.ChainsDb()
    return json.dumps(chaindb.get_questions_given_keyword(key))

@app.route('/question')
def word():
    key = request.args.get('key')
    chaindb = chainsnakedb.ChainsDb()
    return json.dumps(chaindb.get_keyword_given_question(key))

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()
