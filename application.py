from flask import Flask, request, make_response
import sys
import json

application = Flask(__name__)

@application.route('/')
def home():
    return 'hello world'

@application.route("/fulfillment", methods=['POST'])
def fulfillment():
    if request.method == 'POST':
        
        text = {
            "fulfillmentMessages": [
                {
                "text": {
                    "text": [
                    "Text response from webhook"
                    ]
                }
                }
            ]
        }
        
        res = json.dumps(text, indent=4)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        
        return r
        
if __name__ == '__main__':
    application.run()