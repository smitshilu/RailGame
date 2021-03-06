"""
This RailGame skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import csv


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
    if intent_name == "RailGame":
        return RailGame(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent":
        return cancel_response()
    elif intent_name == "AMAZON.StopIntent":
        return stop_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Rail Game skill. " \
                    "Please tell me your 2 locations by saying, " \
                    "Boston to New York"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me your 2 locations by saying something like, " \
                    "Boston to New York"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def RailGame(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user.
    """

    card_title = "RailGame"
    session_attributes = {}
    should_end_session = False
    to_city = ""
    from_city = ""
    
    if ((intent['slots']['to_city']['value'])):
        to_city = (intent['slots']['to_city']['value'])
    else:
        speech_output = "I couldn't find amount for " + from_city +" to " + to_city
        reprompt_text = "Please tell me your 2 locations by saying, " \
            "Boston to New York"
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

    if ((intent['slots']['from_city']['value'])):
        from_city = (intent['slots']['from_city']['value'])
    else:
        speech_output = "I couldn't find amount for " + from_city +" to " + to_city
        reprompt_text = "Please tell me your 2 locations by saying, " \
            "Boston to New York"
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

    from_city1 = from_city.replace(" ", "_")
    to_city1 = to_city.replace(" ", "_")

    data = list(csv.reader(open("payoff.csv")))
    amount = 0
    city_list = ["albany","atlanta","baltimore","billings","birmingham","boston","buffalo","butte","casper","charleston","charlotte","chattenooga","chicago","cincinnati","cleveland","columbus","dallas","denver","des_moines","detroit","el_paso","fargo","fort_worth","houston","indianapolis","jacksonville","kansas_city","knoxville","las_vegas","little_rock","los_angeles","louisville","memphis","miami","milwaukee","minneapolis","mobile","nashville","new_orleans","new_york","norfolk","oakland","oklahoma_city","omaha","philadelphia","phoenix","pittsburgh","pocatello","portland_ma","portland_ore","pueblo","rapid_city","reno","richmond","sacramento","salt_lake_city","san_antonio","san_diego","san_francisco","seattle","shreveport","spokane","st._louis","st._paul","tampa","tucumcari","washington"]
    
    if (from_city1.lower() in city_list and to_city1.lower() in city_list):
        amount = data[city_list.index(from_city1.lower()) + 1][city_list.index(to_city1.lower()) + 1]
    else:
        speech_output = "I couldn't find amount for " + from_city +" to " + to_city
        reprompt_text = "Please tell me your 2 locations by saying, " \
            "Boston to New York"
        return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))
    
    speech_output = "You will get $" + str(amount) + " for " + from_city + " to " + to_city  
    reprompt_text = "You will get $" + str(amount) + " for " + from_city + " to " + to_city
    should_end_session = True
    card_title = "RailGame"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def cancel_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Bye"
    speech_output = "Bye."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def stop_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Bye"
    speech_output = ""
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = ""
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
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
