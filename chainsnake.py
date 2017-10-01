#!flask/bin/python
from flask import Flask

app = Flask(__name__)

@app.route('/hello/<u_name>')
def address(u_name):
	return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()
