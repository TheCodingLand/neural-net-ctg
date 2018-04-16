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

def preparedata(s):
    """
    Given a text, cleans and normalizes it.
    """
    s = s.lower()
    s= s.replace(".","")
    # Replace ips
    s = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' _ip_ ', s)
    # Isolate punctuation, remove numbers
    s = re.sub(r'([\'\"\.\(\)\!\?\-\\\/\,])', r' \1 ', s)
    s = re.sub(r'([0-9])' , ' ', s)
    s = s.replace('*', '')
    s = s.replace('_', '')
    # Remove some special characters
    s = re.sub(r'([\;\:\|•«\n])', ' ', s)

    s = s.replace('&', ' and ')
    s = s.replace('@', ' at ')
    return s

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
    url = 'http://ai-api.lbr.lu/predict'
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
            value = f'{subject!s} {body!s}'.replace('\n',' ').strip()
            value = value.split(' ')
            value = value[0:int(len(value)*75/100)]
            value = ' '.join(value)
            value = preparedata(value)
            
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

            #r = requests.put(url=modurl, json=payloadmod, headers=headers)
