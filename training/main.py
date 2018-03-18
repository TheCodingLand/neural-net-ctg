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
        self.trainfile=""
        self.testfile=""
        self.trainingname=""
        self.trainTestRatio = 95
        self.epochs=20
        self.learningRate=0.2
        self.wordNgrams=3
        self.model = None
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
        
        
        ftdata = open(targetfile, 'w')
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
                
                ftdata.write(txt)
                #logging.info(f"writing : {txt!s} to {targetfile!s}")
        ftdata.close()
        logging.info('finished building fasttext data file')
        self.startTraining(targetfile)


    def preparedata(self, s):
        """
        Given a text, cleans and normalizes it.
        """
        s = s.lower()
        s= s.replace(".","")
        # Replace ips
        s = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' _ip_ ', s)
        # Isolate punctuation
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

            while i < trainingLines:
                logging.info(f"writing in {self.trainfile!s}")
                trainf.write(f.readline())
                i = i+1
            while i < totallines:
                #for testing with pyfasttext, i need to have 1 list of labels and the corresponding liness s
                logging.info(f"writing in {self.testfile!s}")
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

        logging.info(f'Training started with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')
        self.model = FastText()
        self.model = self.model.supervised(input=self.trainfile, output=f"{self.models!s}/{self.trainingname!s}.bin", epoch=self.epochs, lr=self.learningRate, wordNgrams=self.wordNgrams, verbose=2, minCount=1)
        self.test()
        #self.print_results(*model.test(self.testfile))
        logging.info(f'finished training model with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')
        #model.quantize(input=self.trainfile, output=f"{self.models!s}/{self.trainingname!s}.ftz")
        #model.quantize(input=self.trainfile, qnorm=True, retrain=True, cutoff=100000)
        #model.predict_proba_file(self.testfile, k=2)

    def test(self):
        i=0
        correct=0
        with open(self.testfile) as f:
            line = f.readline()
            words = line.split()
            label = words[0]
            line = line.replace(label, '')
            label = label.replace('__', '')
            prediction = self.model.predict(line, k=1)
            logging.info(f"testing gave in {prediction[0]!s}, against {label!s}")
            if prediction[0][0]==label:
                correct=correct+1

            logging.info(f"results : {correct!s}/{i!s}")

time.sleep(1)
logging.info("Starting training")
Training()
