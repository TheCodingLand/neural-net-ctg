import json
import os
import requests

class aimanager(object):

    modelsFolder = '/trainingdata/models/'
    jsonFolder  = '/trainingdata/jsonfiles/'
    textfolder = '/trainingdata/textfiles/'
    configFolder = '/trainingdata/config/'
    #either { "fr" : fileobject } or { "fr" : null}
    language = {}
    ratio = 95

    def __init__(self, config):
        self.modelname = config
        self.config = self.load_config(config)
        #conditional import for ticketing system
        if self.config['tool']=='ot':
            from ai.tools.ticketingsystem import ot as ts
        self.ts = ts()
    
    def load_config(self, config):
        
        configs = json.loads(f'{self.jsonFolder!s}config.json')
        if config in configs.keys():
            return configs[config]

        return config

    def detect(self, text):
        
        langdetect = FastText(f'{self.models!s}/lid.176.bin')
        lang = langdetect.predict_proba_single(text,k=1)
        # we only need to return the first language and probability should be useless at this point.
        # could be used later to default to english ??
        lang = lang[0][0]

        #keeping track on all languages used
        
        return lang

    def splitJson(self, jsondata):

        for entry in jsondata:
            lang = detect(entry['text'])
            if lang not in self.languages.keys():(
                f = open(f'{lang!s}_{self.modelname}.json', 'w')
                self.languages.update({lang: f})
            self.languages[lang].write(entry)
    
    def splitTrainingData(self, jsonfile):
        

        trainjf = open(jsonfile.append(".train"),'w')
        testjf = open(jsonfile.append(".test"),'w')

        jf = json.loads(jsonfile, 'r')
        count = len(jf)
       

        breakpoint = int(count * ratio /100)

        train = jf[0:breakpoint]
        test = jf[breakpoint:-1]
        
        json.dump(train,trainjf)
        json.dump(test,testjf)
        




    def createFastText(self, jsonfile):
       
        j = open(jsonfile, 'r')
        f = open(jsonfile.replace('json','txt'), 'w')
        for entry in json.readlines():

            
            


        
                
            
        

    def getData(self):
        jsondata = self.ts.getTrainingData(self.config['filter'], self.config['label'], self.config['fields'])
        #jsondata is just [ { label : "13241", entry :"text"}]
        return jsondata
            
        



        


        
        





