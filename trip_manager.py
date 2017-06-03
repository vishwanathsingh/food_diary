from __future__ import print_function
from datetime import date
import boto3

dynamodb = boto3.resource('dynamodb')


def lambda_handler(event, context):
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if (event['session']['application']['applicationId'] !=
           "amzn1.ask.skill.99994d95-d8ef-4c96-86b9-e7819cda12af"):
        raise ValueError("Invalid Application ID")

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
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    userId = session['user']['userId'];

    # Dispatch to your skill's intent handlers
    if intent_name == "AddPlace":
        return add_place(intent, userId)
    elif intent_name == "ListTrip":
        return list_trip(intent, userId)
    elif intent_name == "AddTrip":
        return add_trip(intent, userId)
    elif intent_name == "OpenTrip":
        return open_trip(intent, userId)
    elif intent_name == "EditTrip":
        return edit_trip(intent, userId)
    elif intent_name == "DeleteTrip":
        return delete_trip(intent, userId);
    elif intent_name == "SetDate":
        return set_date(intent, userId)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def add_trip(intent, userId):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    tripName = None
    startDate = None
    duration = None
    
    trip_details = {}

    if 'tripName' in intent['slots'] and intent['slots']['tripName'].get('value'):
        tripName = intent['slots']['tripName']['value']
        trip_details['tripname'] = tripName
        trip_details['userId'] = userId
        
        if 'startDate' in intent['slots']:
            startDate = intent['slots']['startDate']['value']
            trip_details['startDate'] = startDate
    
        if 'duration' in intent['slots']:
            duration = intent['slots']['duration']['value']
            trip_details['endDate'] = startDate + duration
        
        save_trip(trip_details)
        speech_output = "I have added your trip " + tripName + \
                        ". You can now add places to your trip by saying, " \
                        " Add Irvine to trip " + tripName
        reprompt_text = ". You can now add places to your trip by saying, " \
                        " Add Irvine to trip " + tripName
        
    else:
        speech_output = "I'm not sure what your trip name is. " \
                        "Please try again."
        reprompt_text = "I'm not sure what your trip name is. " \
                        "You can tell me your trip name by saying, " \
                        "Create trip Memorial Day for 3 days starting on 29th May."
        
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def add_place(intent):
    return

def open_trip(intent, userId=None):
    trip = list_trip(intent['slots']['tripName']['value'])
    if trip is None:
        speech_output = "Trip not found .Please try again."                        
        reprompt_text = "I'm not sure what your trip name is. " \
                        "You can tell me your trip name by saying, " \
                        "Create trip Memorial Day for 3 days starting on 29th May."
    else:
        session_attributes = {}
        speech_output = "Your " + trip['tripname'] + " is starting on " + trip['startDate']
        reprompt_text = "Thank you"
    return build_response(session_attributes, build_speechlet_response(
    	"your upcoming trip", speech_output, reprompt_text, True ))


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Trip Manager"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please talk to me"
    should_end_session = False
    tables = list_trip("someId")
    print (tables)
    speech_output = speech_output
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# dynamo db interactions

def save_trip(trip_details):
    table = dynamodb.Table('TripNames')
    return table.put_item(Item=trip_details)
    
def list_trip(tripname, userId = None):
    table = dynamodb.Table("TripNames")
    return table.get_item(
        Key={
            'tripname': tripname
            }
    ).get('Item')

def edit_details(key, tripid):
    trip = get_trip(tripid)


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
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