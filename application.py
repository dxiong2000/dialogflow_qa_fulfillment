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
     
		print("request recieved")

		text_message = ''
		try:			
			data = request.data
			data_json = json.loads(data)

			query_result = data_json['queryResult']
			lab_test_type = query_result['parameters']['lab_test_type']
			intent_name = query_result['intent']['displayName']
			
			faq_df = pd.read_excel('intents_and_responses.xlsx', sheet_name = 'Sheet1', engine='openpyxl')
	
			faq_df_test_df = faq_df[faq_df['Lab Test Type'] == lab_test_type]
			faq_df_test_df = faq_df_test_df.reset_index(drop=True)
			
			if len(faq_df_test_df) == 0:
				text_message = constants.NO_LAB_TEST_ERROR + ' ' + lab_test_type
			else:
				text_message = faq_df_test_df[intent_name][0]

			if pd.isna(text_message):
				text_message = constants.NO_DATA_FOR_TEST_INTENT_1 + ' ' + lab_test_type + ' ' + constants.NO_DATA_FOR_TEST_INTENT_2 + ' ' + intent_name

			# faq_df_test_intent_df = faq_df_test_df[faq_df_test_df[intent_name]

			# faq_intent_df = faq_df[faq_df['Intent'] == intent_name]
			# faq_intent_param_df = faq_intent_df[faq_intent_df['Parameter'] == param]
			# faq_intent_param_df = faq_intent_param_df.reset_index(drop=True)
			# text_message = faq_intent_param_df['Response'][0]

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


