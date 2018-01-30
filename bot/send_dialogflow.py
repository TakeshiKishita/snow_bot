# -*- coding: utf-8 -*-
import requests, json

class dialogflow_api:
    """
    docstring for dialogflow_api.
    """

    def __init__(self):
        self.base_url = "https://api.dialogflow.com/v1/query?v=20150910"
        self.acces_token = "{YOUR_DIALOG_FLOW_TOKEN}"

    def request_dialogflow(self, message, session_id):
        payload = {"lang": "ja",
                    "query": message,
                    "sessionId": session_id,
                    "timezone": "Asia/Japan"}
        headers = {'content-type': 'application/json;charset=UTF-8','Authorization': 'Bearer '+ self.acces_token}
        ret = requests.post(self.base_url, data=json.dumps(payload), headers=headers)

        return ret.json()

def send_msg(message, session_id):
    a = dialogflow_api()
    return a.request_dialogflow(message, session_id)
