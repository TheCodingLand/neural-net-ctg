import re
import requests
class Ticket(object):
    title = ""
    description =""
    category = ""
    solution = ""
    nRCS = ""
    nDepot = ""
    nCommande = ""
    linkdepot = ""
    linkdossier = ""

    def __init__(self, ticketdata):
        self.title = ticketdata['Title']
        self.description = ticketdata['Description']
        self.solution = ticketdata['SolutionDescription']
        self.date = ticketdata['CreationDate']
        self.category = self.getCategoryTitle(ticketdata['AssociatedCategory'])
        self.nRCS = self.getRcs()
        self.nDepot = self.getNDepot()
        self.nCommande = self.getNCommande()

        if self.nDepot != "":
            self.linkdepot = f'https://mjrcs.intranet.etat.lu/mjrcs-intranet/jsp/secured/DownloadDocumentDepositAction.action?depositYear={self.nDepot[1:3]!s}&depositNumber={self.nDepot[3:10]!s}&documentNumber=0'
        if self.nRCS != "":
            self.linkdossier = f'https://mjrcs.intranet.etat.lu/mjrcs-intranet/jsp/secured/PersonRequestAction.action?ercsNumber={self.nRCS!s}'
        


    def getRcs(self):
        p = r'([A-G]{1}[0-9]{3,7})'
        t = re.search(p, self.title, re.IGNORECASE)
        if t != None:
            return t[0]
        
        t = re.search(p, self.description, re.IGNORECASE)
        if t != None:
            return t[0]
        
        t = re.search(p, self.solution, re.IGNORECASE)
        if t != None:
            return t[0]
        return ""
        
    def getNDepot(self):
        p = r'([L]{1}[0-9]{9})'
        t = re.search(p, self.title, re.IGNORECASE)
        if t != None:
            return t[0]
        
        t = re.search(p, self.description, re.IGNORECASE)
        if t != None:
            return t[0]
        
        t = re.search(p, self.solution, re.IGNORECASE)
        if t != None:
            return t[0]
        return ""
    
    def getNCommande(self):
        p = r'(C_[0-9]{2}_[0-9]{5,9})'
        t = re.search(p, self.title, re.IGNORECASE)
        if t != None:
            return t[0]
        
        t = re.search(p, self.description, re.IGNORECASE)
        if t != None:
            return t[0]
        
        t = re.search(p, self.solution, re.IGNORECASE)
        if t != None:
            return t[0]
        return ""
        

    def getCategoryTitle(self, cat):
        url = f'http://148.110.107.15:5001/api/ot/object/{cat!s}'
        payload = {'requiredfields': ['Title']}
        headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}
        

        r = requests.post(url=url, json=payload, headers=headers)
        data = r.json()
        if data['status'] == "success":
            title = data['data']['Title']
            return title





def getTickets():

    url = 'http://148.110.107.15:5001/api/ot/objects'
    headers = {'Content-type': 'application/json',
                   'Accept': 'text/plain'}


    payload = {
        "objectclass": "Ticket",
        "filter": "last day",
        "variables": [
            {
            }
        ],
        "requiredfields": [
            "Title",
            "Description",
            "SolutionDescription",
            "AssociatedCategory",
            "CreationDate"
        ]
    }
    r = requests.post(url=url, json=payload, headers=headers)
    print (r.status_code)
    data = r.json()
    return data





data = getTickets()
print(data)

tickets= []

for t in data['Ticket']:
    ticket = Ticket(t['data'])
    d={}
    if ticket.nRCS != "" or ticket.nDepot != "" or ticket.nCommande != "":
        d.update({ 'title' :ticket.title, 
                'description':ticket.description.replace(r'\n', ' '),
                'category':ticket.category,
                'solution':ticket.solution.replace(r'\n', ' '),
                'date':ticket.date,
                'rcs':ticket.nRCS,
                'depot':ticket.nDepot,
                'commande':ticket.nCommande,
                'linkdossier' : ticket.linkdossier,
                'linkdepot' : ticket.linkdepot

         })
        tickets.append(d)
    



import json
with open('dump.json', 'w') as outfile:
    json.dump(tickets, outfile)
    