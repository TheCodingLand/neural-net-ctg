import json
import os
import requests
import re
from pyfasttext import FastText
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AiManager(object):

    modelsFolder = '/trainingdata/models/'
    jsonFolder  = '/trainingdata/jsonfiles/'
    textfolder = '/trainingdata/textfiles/'
    configFolder = '/trainingdata/config/'
    #either { "fr" : fileobject } or { "fr" : null}
    languages = {}
    #percentage of the message to keep for prediction
    percentkept=75
    reBuildModel=True
    ratio = 95
    learningRate = 0.2
    epochs = 50
    ngrams = 3
    json=None

    def __init__(self, config, json = None):
        self.modelname = config
        self.config = self.load_config(config)
        #conditional import for ticketing system
        #if self.config['tool']=='ot':
            #from ai.tools.ticketingsystem import ot as ts
        #self.ts = ts()
        

    def train(self, buildJson=False, loadfile=""):
        if loadfile!="":
            try:
                f = open(loadfile, 'r')
                jsonfile = json.load(f)
            except:
                logger.error("failed to load file")
        if buildJson ==True:
            jsonfile = self.getData()
        
        self.splitJson(jsonfile)
        print(self.modelname)
        for language in self.languages.keys():
            self.splitTrainingData(json.load(self.languages[language]))
           
            filename = f'{language!s}_{self.modelname!s}'
            self.createFastText(f'{filename!s}.train')
            self.createFastText(f'{filename!s}.test')
            self.startTraining(f'{filename!s}')
            

    
    def load_config(self, config):
        f=open(f'{self.configFolder!s}config.json' ,'r')
        configs = json.load(f)
        if config in configs.keys():
            return configs[config]

        return config

    def detect(self, text):
        
        langdetect = FastText(f'{self.modelsFolder!s}lid.176.bin')
        lang = langdetect.predict_proba_single(text,k=1)
        # we only need to return the first language and probability should be useless at this point.
        # could be used later to default to english ??
        lang = lang[0][0]
        #keeping track on all languages used
        return lang

    def splitJson(self, jsondata):

        for entry in jsondata:
            lang = self.detect(entry['text'])
            if lang not in self.languages.keys():
                f = open(f'{lang!s}_{self.modelname!s}.json', 'w')
                self.languages.update({lang: f})
            self.languages[lang].write(entry)
    
    def splitTrainingData(self, jsonfile):

        trainjf = open(jsonfile.append(".train"),'w')
        testjf = open(jsonfile.append(".test"),'w')

        jf = json.loads(jsonfile)
        count = len(jf)
       
        breakpoint = int(count * self.ratio /100)

        train = jf[0:breakpoint]
        test = jf[breakpoint:-1]
        
        json.dump(train,trainjf)
        json.dump(test,testjf)

        
    def createFastText(self, jsonfile):
        
        textfile =jsonfile.replace('.json','.txt')
        with open(textfile, 'w') as f:
            for entry in json.loads(jsonfile):
                #logging.error(entry)
                text = entry['text']
                label= entry['label']
                text = self.preparedata(text)
                text = self.removeShort(text)

                #we will not need all the email. Taking 75% of the words should cut most signatures / end of email garbage
                linearray = text.split(' ')
                lwords = len(linearray)
                nbWords= int(lwords*self.percentkept/100)
                text = ' '.join(linearray[0:nbWords])
                txt= f'__label__{label!s} {text!s} \n'
                f.write(txt)
        



    def getData(self):
        jsondata = self.ts.getTrainingData(self.config['filter'], self.config['label'], self.config['fields'])
        #jsondata is just [ { label : "13241", entry :"text"}]
        return jsondata
    
    def removeShort(self, text):
        t = text.split(' ')
        result= []
        for s in t:
            if len(s)>2:
                result.append(s)
        
        result = ' '.join(result)
        return result

    def preparedata(self, s):
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

    def startTraining(self, ftfile):
        
        if self.reBuildModel==True:
            modelfile = ftfile.replace('.txt','')
            logger.info(f'Training started with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.ngrams!s}')
            model = FastText()
            model.supervised(input=ftfile, output=f"{self.modelsFolder!s}/{modelfile!s}", epoch=self.epochs, lr=self.learningRate, wordNgrams=self.ngrams, verbose=2, minCount=1)
            logger.info(f'finished training model with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.ngrams!s}')
            self.test(modelfile)
            #in test mode we will not retrain the model
            
           

    def test(self, modelfilename):
        model= FastText(modelfilename)
        logger('testing')
        
        i=0
        correct=0
        with open(f'{modelfilename!s}.txt.test') as f:
            lines = f.readlines()
            percent = 0
            for line in lines:
                i=i+1
                #logging.info(line)
                words = line.split()
                label = words[0]
                line = line.replace(label, '')
                #logging.info(line)
                label = label.replace('__label__', '')
                prediction = model.predict_proba_single(line, k=1)
                
                #logging.info(f"testing gave in {prediction!s}, against {label!s}")
                #we only return a prediction if confidence is good enough
                #it is a sensitive behaviour to test if the confidence rating is a good indication of success
                if prediction[0][1] > 0.85:
                    if prediction[0][0]==label:
                        
                        correct=correct+1
                        
                    percent = correct/i*100
                    
                else:
                    i=i-1

            logging.info(f"results : {correct!s}/{i!s}, {percent!s}%")

api = AiManager('ot_emails')
api.train(buildJson=False,loadfile='/trainingdata/jsonfiles/data.json')

#data = api.getData()
#f = open(f'{api.modelname!s}.json','w')


        
        





