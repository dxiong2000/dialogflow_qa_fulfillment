from flask import Flask, request, make_response
import sys
import json
import constants
import pandas as pd

application = Flask(__name__)

@application.route('/')
def home():
    return 'hello world'

@application.route("/fulfillment", methods=['POST'])
def fulfillment():

	if request.method == 'POST':

		text_message = ''
		try:			
			data = request.data
			data_json = json.loads(data)

			query_result = data_json['queryResult']		
			param = query_result['parameters']['param-name']
			intent_name = query_result['intent']['displayName']

			faq_df = pd.read_excel('intent_faqs.xlsx', sheet_name = 'Sheet1', engine='openpyxl')
			faq_intent_df = faq_df[faq_df['Intent'] == intent_name]
			faq_intent_param_df = faq_df[faq_df['Parameter'] == param]
			text_message = faq_intent_param_df['Response'][1]

		except KeyError:
			text_message = constants.ERROR_MESSAGE


		reponse_text = {
			"fulfillmentMessages": [
			{
				"text": {
					"text": [
						text_message
					]
				}
				}
			]
		}

		response_json = json.dumps(reponse_text, indent=4)
		response = make_response(response_json)
		response.headers['Content-Type'] = 'application/json'

		return response
        
if __name__ == '__main__':
    application.run()


