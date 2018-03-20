#In this file, each class defines 3 functions used by the solution : 
# - getEmails(), retrieves data to parse and categorize
# - setPredictedCategory(), updates the field in the target tool with the category predicted by the algorithm
# - dumpData() :  applies a filter, and retrieves a large amount of data from the tool. used to generate training and test files.
# should return : {labelfield : "la",  text

# some other utility fonction to help with data can be defined. I needed for example to get the category object's title for omnitracker.
import logging
import requests

class ot(object):
    def __init__(self):
        self.url = 'http://148.110.107.15:5001/api/ot/'
        self.getObjectUrl=  f"{self.url!s}object/"
        self.queryObjectsUrl= f'{self.url!s}objects'
        self.updateObjectUrl = f"{self.url!s}objectmod/"
        self.headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
        self.request = None
        self.labelfield = None

    def getTrainingData(self, filtername, labelfield, fields):

        fields.append(labelfield)
        #filtername="emails last 2 years"
        
        #fields = ["Title","Description",labelfield]
        
        payload = {"objectclass": "Ticket",
            "filter": f"{filtername!s}",
            "variables": [
                {
                }
            ],
            "requiredfields": fields
        }
        try:
            request=requests.post(url=self.queryObjectsUrl, json=payload, headers=self.headers)

        except:

            return False
        
        
        data = request.json()
       
       
        if data['status'] == "success":
            data = data['Ticket']
       
        
        entries = []
        for item in data:
            text = ""

            for field in fields:
                if field !=labelfield:
                    text = text + item[field]
                if field == labelfield:
                    label = item[field]
            
            entry = {label:label, text:text}
            entries.append(entry)
        

        result = { 'entries' : entries }
        return result



        


    def getEmails(self, filtername, fields):
        #this function can be used to pull a large amount of emails based on a filter, and fields
        
        payload = {"objectclass": "Email",
            "filter": f"{filtername!s}",
            "variables": [
                {
                }
            ],
            "requiredfields": fields
        }
        self.request=requests.post(url=self.queryObjectsUrl, json=payload, headers=self.headers)
        self.handleResult()

    def getOject(self, ref):
        ref = ref.replace("__label__", "")
        self.request_url = f"{self.getObjectUrl!s}{ref!s}"
        payload = {'requiredfields': ['Title']}
        self.request=requests.post(url=self.request_url, json=payload, headers=self.headers)
        self.handleResult()

    def setPredictedCategory(self, id, category):
        self.request_url = f"{self.updateObjectUrl!s}{id!s}"
        payload = { 'PredictedCategory' : f'{category!s}' }
        self.request=requests.post(url=self.request_url, json=payload, headers=self.headers)
        self.handleResult() 

    def handleResult(self):
        #logging.error(dir(self.request))
        result = self.request.json()
        #logging.error(result)
        if result['status'] == "success":
            data = result['Ticket']    
            return data
        
        return result
    
    def getCategoryTitle(self, cat):

        payload = {'requiredfields': ['Title']}
        predicted_url = f'{self.getObjectUrl!s}{cat!s}'

        r = requests.post(url=predicted_url, json=payload, headers=self.headers)
        data = r.json()
        if data['status'] == "success":
            title = data['data']['Title']
            return title
        