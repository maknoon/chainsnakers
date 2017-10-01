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

@app.route('/test_watson')
def test_watson():
    response = sem.analyze(
        url="https://quizlet.com/229277915/biology-flash-cards/",
        features=[
            Features.SemanticRoles(
            # Semantic Roles options
            )
        ]
    )
    response_dict = json.dumps(response, indent=2)




@app.route('/hello/<u_name>')
def address(u_name):
    return 'hey {}! did you know that harris is gay'.format(u_name)

@app.route('/')
def index():
    return "ssssssssss"

if __name__ == '__main__':
    app.run()
