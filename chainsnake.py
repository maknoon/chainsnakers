#!~/usr/bin/python3
<<<<<<< HEAD
<<<<<<< 5febe1714bf0516a4c77466c7995cda9b660acef
<<<<<<< 6299b34544663d4e73d656e7927cfecaf93be8cd
from flask import Flask
#import pymysql
import json
import config
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features
=======
from flask import Flask, request
import pymysql
import json
>>>>>>> lambda connected to API
=======
from flask import Flask, request
import pymysql
import json
>>>>>>> lambda connected to API
=======
from flask import Flask, request
import pymysql
import json
>>>>>>> 6acb29c01fab5dd2b874b8f96a6b64c139c0cae8

app = Flask(__name__)
sem = NaturalLanguageUnderstandingV1(
  username=config.watson_u,
  password=config.watson_p,
  version=config.watson_d)
# return answer and question keywords
@app.route('/test_watson')
def test_watson():

    text = "An organization of workers that tries to improve working conditions, wages, and benefits for its members"
    if len(text) < 15:
        answer = text
    else:
        answer = sem.analyze(
            text="An organization of workers that tries to improve working conditions, wages, and benefits for its members",
            features=[
                Features.Keywords(
                # Semantic Roles options
                )
            ]
        )
    text="Social Justice"
    if len(text) < 15:
        question = text
    else:
        question = sem.analyze(
            text="Social Justice",
            features=[
                Features.Keywords(
                # Semantic Roles options
                )
            ]
        )
    return(json.dumps(answer, indent=2))
    return(json.dumps(question, indent=2))
#return single search term given alexa question
@app.route('/test_searchterm')
def text_searchterm():
    text = "tell me about social justice and obama?"
    if len(text) < 15:
        keywords = text
    else:
        keywords = sem.analyze(
            text="tell me about social Justice and obama",
            features=[
                Features.Keywords(
                # Semantic Roles options
                )
            ]
        )

    dictionary = (json.dumps(keywords, indent=2))
    keyword = keywords["keywords"][0]["text"]
    return(keyword)



@app.route('/setup')
def fetch():
    set_to_fetch = request.args.get('fetch')

    return json.dumps({"message": "fetched the {} set!".format(set_to_fetch)},indent=2)

@app.route('/setup')
def fetch():
    set_to_fetch = request.args.get('fetch')

    return json.dumps({"message": "fetched the {} set!".format(set_to_fetch)},indent=2)

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
