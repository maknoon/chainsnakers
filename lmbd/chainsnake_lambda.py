"""
amazon lambda sysquiz function
"""
from __future__ import print_function
import os, urllib2, json

# --------------- env vars + some strings -> API queries ----------------------
snake_srvr_ip = os.environ["SNAKE_SRVR"]
fetch_new_set_url = "{0}/setup?fetch={1}"

# --------------- HERE ARE THE HELPER CALLS TO SNAKE./.. ----------------------
# returns a JSON object of sets from the SNAKE SERVER
def get_set_from_srvr(system_to_fetch):
    url = fetch_new_set_url.format(snake_srvr_ip,system_to_fetch)
    response = urllib2.urlopen(url)
    data = dict(json.loads(response.read()))
    msg = data['message']

    return msg


# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the System Learning Module. " \
                    "Please tell me what system you would like to learn by saying, " \
                    "teach me about biology"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me what system you would like to learn by saying, " \
                    "teach me about biology."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the System Learning with Alexa. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_system_set_attributes(system_set):
    return {"systemSet": system_set}


def set_system_in_session(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'System' in intent['slots']:
        system_set = intent['slots']['System']['value']
        session_attributes = create_system_set_attributes(system_set)

        # API call to fetch & generate the set of cards
        srvr_resp = get_set_from_srvr(system_set)

        speech_output = srvr_resp + \
                        "Let's begin learning about " + \
                        system_set + \
                        ". You can ask me more about " + \
                        system_set + \
                        " by asking, " \
                        "what's next?"
        reprompt_text = "You can ask me to repeat by saying, " \
                        "could you repeat"
    else:
        speech_output = "I'm not sure what system you are talking about. " \
                        "Please try again."
        reprompt_text = "I'm not sure what system you are talking about. " \
                        "You can tell me what system you would like to learn by saying, " \
                        "teach me about biology."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_system_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None

    if session.get('attributes', {}) and "systemSet" in session.get('attributes', {}):
        system_set = session['attributes']['systemSet']
        speech_output = "The system we are studying is " + system_set + \
                        ". Goodbye."
        should_end_session = True
    else:
        speech_output = "I'm not sure what system you are talking about. " \
                        "You can say, teach me about biology."
        should_end_session = False

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "FetchNewSystemIntent":
        return set_system_in_session(intent, session)
    elif intent_name == "WhatsNextIntent":
        return get_system_from_session(intent, session)
    elif intent_name == "WhatsBeforeIntent":
        return get_system_from_session(intent, session)
    elif intent_name == "WhatsSimilarIntent":
        return get_system_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])