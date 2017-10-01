#!~/usr/bin/python3
from flask import Flask
import pymysql

app = Flask(__name__)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()
