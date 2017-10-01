#!~/usr/bin/python3
from flask import Flask
#import pymysql
import json
import config
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as Features

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



@app.route('/hello/<u_name>')
def address(u_name):
    return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()