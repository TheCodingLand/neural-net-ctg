import logging
import os
import subprocess
from pyfasttext import FastText
import glob
import json
import re
import time

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
        self.epochs=200
        self.learningRate=0.2
        self.wordNgrams=3
        self.loadjson()

    

    def loadjson(self):

        jsonfiles = glob.glob("/trainingdata/jsonfiles/*.json")
        for jsonfile in jsonfiles:
            data = json.load(open(jsonfile))
            print(jsonfile)
            self.trainingname = jsonfile.split('/')[-1].replace('.json','')
            print(self.trainingname)
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
        print('created file')

        for entry in data:
            logging.error(entry)
            subject = entry['data']['Title']
            body = entry['data']['Description']
            category= entry['data']['AssociatedCategory']
            subject = self.preparedata(subject)
            body = self.preparedata(body)
            fulltext= f'{subject!s} {body!s}'
            fulltext = self.removeShort(fulltext)
            #we will not need all the email. Taking 75% of the words should cut most signatures / end of email garbage
            linearray = fulltext.split(' ')
            lwords = len(linearray)
            nbWords= int(lwords*75/100)
            fulltext = ' '.join(linearray[0:nbWords])
            txt= f'__label__{category!s} {fulltext!s} \n'
            if len(txt.split()) > 10:
                ftdata.write(txt)
        ftdata.close()
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
        s = s.replace('*', '')
        s = s.replace('_', '')
        # Remove some special characters
        s = re.sub(r'([\;\:\|•«\n])', ' ', s)

        # Replace numbers and symbols with language
        s = s.replace('&', ' and ')
        s = s.replace('@', ' at ')
        s = s.replace('0', ' zero ')
        s = s.replace('1', ' one ')
        s = s.replace('2', ' two ')
        s = s.replace('3', ' three ')
        s = s.replace('4', ' four ')
        s = s.replace('5', ' five ')
        s = s.replace('6', ' six ')
        s = s.replace('7', ' seven ')
        s = s.replace('8', ' eight ')
        s = s.replace('9', ' nine ')

    def splitTestData(self, ftfile):
        i=-1
        with open(ftfile) as f:
            for i, l in enumerate(f):
                pass
        trainingLines = int(i*self.trainTestRatio/100)
        self.testfile = f"{ftfile!s}.test"
        self.trainfile = f"{ftfile!s}.train"
        testf = open(self.testfile, 'w')
        trainf = open(self.trainfile, 'w')
        i = -1
        with open(ftfile) as f:
            if i < trainingLines:
                trainf.write(ftfile.readline())
            else:
                testf.write(ftfile.readline())


    def print_results(self, N, p, r):
        print("N\t" + str(N))
        print("P@{}\t{:.3f}".format(1, p))
        print("R@{}\t{:.3f}".format(1, r))

    def startTraining(self, ftfile):
        self.splitTestData(ftfile)

        logging.error(f'Training started with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')

        model = FastText.train_supervised(input=self.trainfile, epoch=self.epochs, lr=self.learningRate, wordNgrams=self.wordNgrams, verbose=2, minCount=1)
        #self.print_results(*model.test(self.completefile))
        logging.error(f'finished training model with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')
        model.save_model(f"{self.models!s}/{self.trainingname!s}.bin")
        self.print_results(*model.test(self.testfile))
        model.quantize(input=self.trainfile, qnorm=True, retrain=True, cutoff=100000)
        self.print_results(*model.test(self.testfile))
        model.save_model(f"{self.models!s}/{self.trainingname!s}.ftz")
        
while True:
    time.sleep(15)
    print("Starting training")
    Training()
