#DRAFT DEBUG/TESTING
            
import requests
import time
import os

def getCategoryTitle(cat):
    c_url = 'http://148.110.107.15:5001/api/ot/object/'
    c_headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
    c_payload = {'requiredfields': ['Title']}
    predicted_url = f'{c_url!s}{cat!s}'
    r = requests.post(url=predicted_url, json=c_payload, headers=c_headers)
    data = r.json()
    if data['status'] == "success":
        title = data['data']['Title']
        return title


def getEmails():

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
    r = requests.post(url=url, json=payload, headers=headers)
    print (r.status_code)
    data = r.json()
    return data


def predict(text):
    url = 'http://148.110.107.15/api/predict'
    headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
    payload = {"text": text }
    prediction = requests.post(url=url, json=payload, headers=headers)
    return prediction

while True:
    time.sleep(10)
    data = getEmails()
    print (data['status'])
    if data['status'] == "success":
        for email in data['Email']:
            id = email['id']
            subject=email['data']['Subject']
            body = email['data']['Body Plain Text']
            value = f'{subject!s}{body!s}'.replace('\n',' ').strip()
            value = value.split(' ')
            value = value[0:int(len(value)*75/100)]
            value = ' '.join(value)
            
            print(value)
            prediction = predict(value)
            

            prediction = prediction.json()
            print(prediction)
            prediction1 = prediction['results']['category']

            prediction2 = prediction['results']['category2']




            print (prediction1)

            categ_title=getCategoryTitle(prediction1).split(':')[-1].strip()
            if categ_title =="":
                categ_title=getCategoryTitle(prediction1).strip()
            prediction = categ_title

            categ_title=getCategoryTitle(prediction2).split(':')[-1].strip()
            if categ_title =="":
                categ_title=getCategoryTitle(prediction2).strip()
            prediction2 = categ_title
            
            

            modurl=f'http://148.110.107.15:5001/api/ot/objectmod/{id!s}'
            print(modurl)
            payloadmod = { 'PredictedCategory' : f'{prediction!s} / {prediction2!s}' }
            print (payloadmod)
            headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}

            r = requests.put(url=modurl, json=payloadmod, headers=headers)
