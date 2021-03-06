#!~/usr/bin/python

import config
import urllib2
import json
import requests
# from requests_oauthlib import OAuth2Session
import operator

import watsonNLU
import chainsnakedb as cdb


# --- URL Requests ---
def run():

    # Search
    searchURL = 'https://api.quizlet.com/2.0/search/sets?client_id='
    q = raw_input("Topic: ")
    # q = "spanish"
    while (q == ""):
        q = raw_input("Try again: ")
    term = raw_input("Term (not required): ")
    # term = "silla"

    print "Searching Sets by matching subject/topic"
    requestSearch = urllib2.urlopen(searchURL+config.qclient_id+"&q=%s&term=%s"%(q, term))
    jsonStringSearch = requestSearch.read()
    parsedJsonSearch = json.loads(jsonStringSearch)
    if (parsedJsonSearch["total_results"] == 0):
        print "No results found"
    else:
        print json.dumps(parsedJsonSearch, indent=2)
        print "\n-----------\n"
        # # DB reset & repopulate
        chainsDb.reset_db()
        chainsDb.insert_to_topics(q)
        # follow-up
        retrieveIdTc(parsedJsonSearch)

def retrieveIdTc(parsedJson):

    parsedJsonSearch = parsedJson
    print "Retieving ID & Term-count pairs of resulting Sets\n"
    resultSetsIdTc = {}
    for numSet in parsedJsonSearch["sets"]:
        resultSetsIdTc[numSet["id"]] = numSet["term_count"]
    print resultSetsIdTc
    print "\n-----------\n"

    print "Sorting dictionary by Term-count\n"
    sortedResultSet = sorted(resultSetsIdTc.items(), key=operator.itemgetter(1))
    print sortedResultSet
    print "\n-----------\n"

    print "Retrieving SetID of Set with lowest Term-count\n"
    setID = sortedResultSet[0][0]
    print setID
    # setID = "106176371"
    fetchSet(setID)

def fetchSet(ID):

    setID = ID
    # Set
    setURL = 'https://api.quizlet.com/2.0/sets/%s?client_id='%(setID)
    print "\n-----------\n"

    print "Retrieving Set\n"
    requestSet = urllib2.urlopen(setURL+config.qclient_id)
    jsonStringSet = requestSet.read()
    parsedJsonSet = json.loads(jsonStringSet)
    if (parsedJsonSet == ""):
        print "Set not found"
    else:
        print json.dumps(parsedJsonSet, indent=2)
        print "\n-----------\n"
        retrieveTD(parsedJsonSet)

def retrieveTD(parsedJson):

    parsedJsonSet = parsedJson
    print "Retrieving Term & Definition pairs of resulting Terms in Set\n"
    resultTerms = {}
    for numTerms in parsedJsonSet["terms"]:
        resultTerms[numTerms["term"]] = numTerms["definition"]
        # # populate terms & definitions
        chainsDb.insert_to_card(resultTerms[numTerms["term"]], numTerms["definition"])
    print resultTerms
    print "\n-----------\n"
    watsonNLUkw(resultTerms)

def watsonNLUkw(resultTD):

    resultTerms = resultTD
    # --- Watson NLU: Q&A for Keyword(s) ---
    strJsonKW = ""
    for keys, values in resultTerms.iteritems():
        # jsonKW += json.dumps(watsonNLU.test_watson(keys, values), indent=2)
        strJsonKW += watsonNLU.test_watson(keys, values)
    jsonKW = json.dumps(strJsonKW)
    parsedJsonKW = json.loads(jsonKW)
    # print jsonKW
    print parsedJsonKW
    print "\n-----------\n"
    # for k in parsedJsonKW.keys(): print k


chainsDb = cdb.ChainsDb()
run()


# --- OAuth --------------------------------------

# Quizlet OAuth2 endpoints 
auth_url = 'https://quizlet.com/authorize'
# authorization_base_url = "https://quizlet.com/authorize?client_id=%s&response_type=code&scope=read\%20write_set" %(config.qclient_id)
token_url = 'https://api.quizlet.com/oauth/token'

# # Quizlet auth code
# # example url: "https://quizlet.com/authorize?response_type=code&client_id=%s&scope=read&state=string" %(config.qclient_id)
# def get_code():
#     req_body = {'scope': 'read',
#                 'client_id': config.qclient_id,
#                 'response_type': 'code',
#                 'state': 'STATE',
#                 'redirect_uri': config.qredirect_uri,
#     }
#     res = requests.get(auth_url, data=req_body)
#     return res.json()

# # Quizlet OAuth2
# def get_oauth2_token():
#     head = {'Content-Type': 'application/x-www-form-urlencoded',
#             'Authorization': 'Basic UG53cHl0cnNxVjpqcXNmNU1ieHdGNXZ4N3laQ1dyQUVE'}

#     # build POST request body
#     req_body = {'grant_type': 'authorization_code',
#                 'code': '',
#                 'redirect_uri': config.qredirect_uri,
#                 'client_id': config.qclient_id,
#                 'client_secret': config.qclient_secret}
#     res = requests.post(token_url, headers=head, data=req_body, verify=True)
#     return 'Bearer ' + res.json()['access_token']

def getQuizlet():
    head = {'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + config.qToken}

    req_body = {'client_id': config.qclient_id,
                'redirect_uri': config.qredirect_uri}

    # # build search query parameters
    # qp = {'latitude': latitude,}

    res = requests.get(searchURL, headers=head, verify=True)

    #json.dumps(r.json(),indent=2,separators=(',',':'))
    return res.json()

# print get_code()
# print get_oauth2_token()
# print getQuizlet()


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