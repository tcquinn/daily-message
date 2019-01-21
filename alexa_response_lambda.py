from message_database import MessageStoreS3 as MessageStore

def lambda_handler(event, context):
    print('Received request')
    message_store = MessageStore()
    print('event.session.application.applicationId={}'.format(
        event['session']['application']['applicationId']))

    if event['session']['new']:
        print('on_session_started requestId={}, sessionId={}'.format(
                event['request']['requestId'],
                event['session']['sessionId']))

    if event['request']['type'] == "LaunchRequest":
        print('on_launch requestId={}, sessionId={}'.format(
                 event['request']['requestId'],
                 event['session']['sessionId']))
        return welcome_response()

    elif event['request']['type'] == "IntentRequest":
        print('on_intent requestId={}, sessionId={}'.format(
                 event['request']['requestId'],
                 event['session']['sessionId']))
        intent_name = event['request']['intent']['name']
        if intent_name == "SayWhyMargaretIsAwesome":
            message = message_store.get_message()
            output = 'This one is from {}. {}'.format(
                message['contributor'],
                message['body'])
            return build_response(
                session_attributes = {},
                speechlet_response = build_speechlet_response(
                    title = 'Margaret is Awesome',
                    output = output,
                    reprompt_text = None,
                    should_end_session = True))
        elif intent_name == "AMAZON.HelpIntent":
            return welcome_response()
        elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
            return build_response(
                session_attributes = {},
                speechlet_response = build_speechlet_response(
                    tile = "Session Ended",
                    output = "Okay, but Margaret is still awesome",
                    reprompt_text = None,
                    should_end_session = True))
        else:
            raise ValueError("Invalid intent")

    elif event['request']['type'] == "SessionEndedRequest":
        session_ended_request = event['request']
        session = event['session']
        print('on_session_ended requestId={}, sessionId={}'.format(
            event['request']['requestId'],
            event['session']['sessionId']))

def welcome_response():
        return build_response(
            session_attributes = {},
            speechlet_response = build_speechlet_response(
                title = "Margaret is Awesome",
                output = "Ask me why Margaret is awesome",
                reprompt_text = "Try saying why is Margaret awesome",
                should_end_session = False))

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

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
