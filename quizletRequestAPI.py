#!~/usr/bin/python

import config
import json

import requests
# from requests_oauthlib import OAuth2Session

# Quizlet OAuth2 endpoints 
auth_url = 'https://quizlet.com/authorize'
# authorization_base_url = "https://quizlet.com/authorize?client_id=%s&response_type=code&scope=read\%20write_set" %(config.qclient_id)
token_url = 'https://api.quizlet.com/oauth/token'

# Quizlet auth code
# example url: "https://quizlet.com/authorize?response_type=code&client_id=%s&scope=read&state=string" %(config.qclient_id)
def get_code():
    req_body = {'scope': 'read',
                'client_id': config.qclient_id,
                'response_type': 'code',
                'state': 'STATE',
                'redirect_uri': config.qredirect_uri,
    }
    res = requests.get(auth_url, data=req_body)
    return res.json()

# Quizlet OAuth2
def get_oauth2_token():
    head = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic UG53cHl0cnNxVjpqcXNmNU1ieHdGNXZ4N3laQ1dyQUVE'}

    # build POST request body
    req_body = {'grant_type': 'authorization_code',
                'code': 'jnBhz3BR7e5V8PuK7MmdF7F5Tv9xXuNwUezyjdxH',
                'redirect_uri': config.qredirect_uri,
                'client_id': config.qclient_id,
                'client_secret': config.qclient_secret}
    res = requests.post(token_url, headers=head, data=req_body, verify=True)
    
    print res.json()
    return 'Bearer ' + res.json()['access_token']

def getQuizletUser():
    head = {'Content-Type': 'application/json',
            'Authorization': get_oauth2_token()}

    # # build search query parameters
    # qp = {'latitude': latitude,}

    res = requests.get(searchURL, headers=head, verify=True)

    #json.dumps(r.json(),indent=2,separators=(',',':'))
    return res.json()

# print get_code()
print get_oauth2_token()
# print getQuizletUser()


# Quizlet OAuth2Session
# quizlet = OAuth2Session(config.qclient_id, redirect_uri=config.qredirect_uri)

# # Redirect user for authorization
# authorization_url, state = quizlet.authorization_url(authorization_base_url)
# print 'Please go here and authorize,', authorization_url

# # Get the authorization verifier code from the callback url
# redirect_response = raw_input('Paste the full redirect URL here:')

# # Fetch the access token
# quizlet.fetch_token(token_url, client_secret=client_secret, authorization_response=redirect_response)

# # Fetch a protected resource, i.e. user profile
# req = quizlet.get('https://api.quizlet.com/2.0/users/mlhhack?whitespace=1')
# print req.content


# URL Request
# import urllib2
# request = urllib2.urlopen('https://api.quizlet.com/2.0/sets/415?whitespace=1')
# json_string = request.read()
# parsed_json = json.loads(json_string)
# str_parsed_json = json.dump(json_string)
# location = parsed_json['current_observation']['display_location']['full']
# print "%s" %(location)

