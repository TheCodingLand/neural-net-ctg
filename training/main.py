import logging
import os
import subprocess
from pyfasttext import FastText
import glob
import json
import re
import time

logging.basicConfig(level=logging.INFO)
labelFields=[]
fields = []
filename = ""



#we could  get a filename, fields to get training data from
#and fields containing labels for supervised learning ?
# json -> fasttext data -> vec -> quantize


class Training(object):

    textfiles = "/trainingdata/textfiles"
    models = "/trainingdata/models"
    
    def __init__(self):
        self.testing=True
        self.trainfile=""
        self.testfile=""
        self.trainingname=""
        self.trainTestRatio = 95
        self.epochs=200
        self.learningRate=0.2
        self.wordNgrams=3
        self.model = None
        
        self.languages=dict()
        
        self.loadjson()
    

        
            

    def loadjson(self):

        jsonfiles = glob.glob("/trainingdata/jsonfiles/*.json")
        for jsonfile in jsonfiles:
            data = json.load(open(jsonfile))
            logging.info(jsonfile)
            self.trainingname = jsonfile.split('/')[-1].replace('.json','')
            logging.info(self.trainingname)
            targetfile = f"{self.textfiles!s}/{self.trainingname!s}.txt"
            self.makeFastText(data, targetfile)

    def removeShort(self, text):
        t = text.split(' ')
        result= []
        for s in t:
            if len(s)>1:
                result.append(s)
        
        result = ' '.join(result)
        return result

    def makeFastText(self, data, targetfile):
        
        langdetect = FastText(f'{self.models!s}/lid.176.bin')

        #ftdata = open(targetfile, 'w')
        logging.info('created file')

        for entry in data['Ticket']:
            
            subject = entry['data']['Title']
            body = entry['data']['Description']
            category= entry['data']['AssociatedCategory']
            subject = self.preparedata(subject)
            body = self.preparedata(body)
            fulltext = f'{subject!s} {body!s}'
            fulltext = self.removeShort(fulltext)
            #we will not need all the email. Taking 75% of the words should cut most signatures / end of email garbage
            linearray = fulltext.split(' ')
            lwords = len(linearray)
            nbWords= int(lwords*90/100)
            fulltext = ' '.join(linearray[0:nbWords])
            txt= f'__label__{category!s} {fulltext!s} \n'
            #logging.info(txt)
            
            if len(txt.split()) > 10:
                lang = langdetect.predict_proba_single(fulltext,k=1)
                #logging.info(f'predicted {lang[0][0]!s}')
                if lang[0][0] not in self.languages.keys():
                    self.languages.update({ lang[0][0] : [txt,] })
                else:
                    #logging.info(self.languages[lang[0][0]])
                    self.languages[lang[0][0]].append(txt)
        for lang in self.languages.keys():
            f = open(f'{self.textfiles!s}/{lang!s}_{self.trainingname!s}.txt', 'w')
            for line in self.languages[lang]:
                f.write(line)
            f.close()
                
                #logging.info(f"writing : {txt!s} to {targetfile!s}")
        
        logging.info(f'finished building fasttext data file,languages : {self.languages.keys()!s}')
        trainingname=self.trainingname
        for language in self.languages.keys():
            self.trainingname=f'{language}_{trainingname}'
            self.startTraining(f'{self.textfiles!s}/{self.trainingname!s}.txt')


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

    def splitTestData(self, ftfile):
        logging.info(f'splitting {ftfile!s}')
        i = sum(1 for line in open(ftfile))
        logging.info(f'lines : {i!s}')
        totallines=i
        trainingLines = int(totallines*self.trainTestRatio/100)
        logging.info(f"TOTAL training lines : {trainingLines!s}")
        self.testfile = f"{ftfile!s}.test"
        
        self.trainfile = f"{ftfile!s}.train"
        
        testf = open(self.testfile, 'w')
        trainf = open(self.trainfile, 'w')
        i = 0
        with open(ftfile) as f:
            logging.info(f"writing in {self.trainfile!s}")
            while i < trainingLines:
                
                trainf.write(f.readline())
                i = i+1
            logging.info(f"writing in {self.testfile!s}")
                
            while i < totallines:
                #for testing with pyfasttext, i need to have 1 list of labels and the corresponding liness s
                testf.write(f.readline())
                i = i+1
           
        trainf.close()
        testf.close()

    def print_results(self, N, p, r):
        logging.info("N\t" + str(N))
        logging.info("P@{}\t{:.3f}".format(1, p))
        logging.info("R@{}\t{:.3f}".format(1, r))

    def startTraining(self, ftfile):
        
        self.splitTestData(ftfile)
        if self.testing==False:

            logging.info(f'Training started with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')
            self.model = FastText()
            self.model.supervised(input=self.trainfile, output=f"{self.models!s}/{self.trainingname!s}", epoch=self.epochs, lr=self.learningRate, wordNgrams=self.wordNgrams, verbose=2, minCount=1)
            logging.info(f'finished training model with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')
            
            self.test()
        else:
            #in test mode we will not retrain the model
            logging.info(f'loading {self.models!s}/{self.trainingname!s}.bin')
            self.model = FastText(f'{self.models!s}/{self.trainingname!s}.bin')
            self.test()
        #self.print_results(*model.test(self.testfile))
        #model.quantize(input=self.trainfile, output=f"{self.models!s}/{self.trainingname!s}.ftz")
        #model.quantize(input=self.trainfile, qnorm=True, retrain=True, cutoff=100000)
        #model.predict_proba_file(self.testfile, k=2)

    def test(self):
        i=0
        correct=0
    

        with open(self.testfile) as f:
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
                prediction = self.model.predict_proba_single(line, k=1)
                
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

time.sleep(1)
logging.info("Starting training")
Training()

#settings all data single result:
#self.trainTestRatio = 95 self.epochs=200 self.learningRate=0.2 self.wordNgrams=3
#results: 1018/1614
#all data 2 predictions:
#root:results : 1118/1614, 69.26889714993804%
# 687/945, 72.6984126984127% sur le francais uniquement
# 320/492, 65.04065040650406% sur l'anglais


#when filtering > 75% confidence, I get 535/650, 82.3076923076923% for french data, and 249/289, 86.159169550173% for english
#when filtering > 85% confidence, I get the results below:
    #517/602, 85.88039867109634% french
    #29/36, 80.55555555555556% german
    #238/270, 88.14814814814815% english

#need to make graphs to get best ratio predictiontotal/confidence/percentage of errors, 
