#!~/usr/bin/python
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
def test_watson(t, t2):

    # text = "An organization of workers that tries to improve working conditions, wages, and benefits for its members"
    text = t
    if len(text) < 15:
        answer = text
    else:
        answer = sem.analyze(
            # text="An organization of workers that tries to improve working conditions, wages, and benefits for its members",
            text = t,
            features=[
                Features.Keywords(
                # Semantic Roles options
                )
            ]
        )
    # text2 ="Social Justice"
    text2 = t2
    if len(text2) < 15:
        question = text2
    else:
        question = sem.analyze(
            # text="Social Justice",
            text = t2,
            features=[
                Features.Keywords(
                # Semantic Roles options
                )
            ]
        )
    return(json.dumps(answer, indent=2))+(json.dumps(question, indent=2))
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

@app.route('/hello/<u_name>')
def address(u_name):
    return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()