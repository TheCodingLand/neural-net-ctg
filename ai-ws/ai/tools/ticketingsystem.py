#In this file, each class defines 3 functions used by the solution : 
# - getEmails(), retrieves data to parse and categorize
# - setPredictedCategory(), updates the field in the target tool with the category predicted by the algorithm
# - dumpData() :  applies a filter, and retrieves a large amount of data from the tool. used to generate training and test files.


# some other utility fonction to help with data can be defined. I needed for example to get the category object's title for omnitracker.

import requests

class ot(object):
    def __init__(self):
        self.url = 'http://148.110.107.15:5001/api/ot/'
        self.getObjectUrl=  f"{self.url!s}object/"
        self.queryObjectsUrl= f'{self.url}objects/'
        self.updateObjectUrl = f"{self.url!s}objectmod/"
        self.headers = {'Content-type': 'application/json',
                    'Accept': 'text/plain'}
        self.request = None

    def getTrainingData(self):
        filtername="all email tickets"
        fields = ['Title','Description','AssignedCategory']
        payload = {"objectclass": "Ticket",
            "filter": f"{filtername!s}",
            "variables": [
                {
                }
            ],
            "requiredfields": fields
        }
        
        self.request=requests.post(url=self.queryObjectsUrl, json=payload, headers=self.headers)
        self.handleResult()



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
        result = self.request.json()
        if result['status'] == "success":
            data = result['data']    
            return data
        