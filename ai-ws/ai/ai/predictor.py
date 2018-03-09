
import requests
import time
import os
from fastText.FastText import load_model


class predictor(object):
    def __init__(self):
        self.model = load_model("emails.ftz")

    def getSentence(self):
        print("getsentence")

    def getCategoryTitle(self, cat):

        c_payload = {'requiredfields': ['Title']}
        predicted_url = f'{c_url!s}{cat!s}'

        r = requests.post(url=predicted_url, json=c_payload, headers=HEADERS)
        data = r.json()
        if data['status'] == "success":
            title = data['data']['Title']
            return title

    def run_prediction(self, email):
        return model.predict(email, k=1)


#print (pred.testValue("Dear Sir/Madam,Having spoken to your colleague earlier today, we are facing challenges filing the annual accounts.please find attached the excel version of the annual accounts.Many thanks for your help.Kind regards Rachelle Aloko"))

url = 'http://148.110.107.15:5001/api/ot/objects'
headers = {'Content-type': 'application/json',
           'Accept': 'text/plain'}


payload = {
    "objectclass": "Email",
    "filter": "today email",
    "variables": [
        {
        }
    ],
    "requiredfields": [
        "Subject",
        "Body Plain Text"
    ]
}


while True:
    time.sleep(10)
    r = requests.post(url=url, json=payload, headers=headers)
    print(r.status_code)
    data = r.json()
    print(data['status'])
    if data['status'] == "success":
        for email in data['Email']:
            id = email['id']
            subject = email['data']['Subject']
            body = email['data']['Body Plain Text']
            value = f'{subject!s}{body!s}'[:400].replace('\n', ' ').strip()
            print(value)
            prediction = run_prediction(value)
            prediction = prediction[0][0].replace('__label__', '')
            print(prediction)

            categ_title = getCategoryTitle(prediction).split(':')[-1].strip()
            if categ_title == "":
                categ_title = getCategoryTitle(prediction).strip()
            prediction = categ_title
            modurl = f'http://148.110.107.15:5001/api/ot/objectmod/{id!s}'
            print(modurl)
            payloadmod = {'PredictedCategory': f'{prediction!s}'}
            print(payloadmod)

            r = requests.put(url=modurl, json=payloadmod, headers=headers)
