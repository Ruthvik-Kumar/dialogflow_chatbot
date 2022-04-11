from flask import Flask, request
from flask_cors import CORS, cross_origin
#from google.cloud import dialogflow
from google.cloud import dialogflow_v2beta1 as dialogflow

project_id = 'newagent-hvgx'
session_id = '123456789'  # generate random
language_code = 'en-US'

app = Flask(__name__)
CORS(app)

# geting and sending response to dialogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
# processing the request from dialogflow
def processRequest():

    event_data = request.get_json(force=True,silent=True)

    if event_data['type'] == 'CARD_CLICKED':
        action_name = event_data['action']['actionMethodName']
        resp, button = detect_intent_texts(text=action_name)

    # if (req.body.type == "CARD_CLICKED"):
    #   action_name = req.body.action.actionMethodName

    return resp, button


def detect_intent_texts(text, project_id='newagent-hvgx', session_id='123456789', language_code='en-US'):
    """Returns the result of detect intent with texts as inputs.
        Using the same `session_id` between requests allows continuation
        of the conversation."""

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    # output_text = response.query_result.fulfillmentText
    # payload = response.query_result.fulfillmentMessages.payload
    output = response.query_result.fulfillmentMessages
    output_text, payload = output[0], output[1]["payload"]

    return output_text, payload


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')