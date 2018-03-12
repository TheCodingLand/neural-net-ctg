#this class can be used in two modes : learning or processing
#learning file will be in format :
#__label__category and a sentence that should be assigned to it \n
#another format possible :
#__label__category1 __label__category2 a sentence that should be assigned to both categories
#can be extended to support other ticketing systems later
import logging
import re
import os
from fastText import train_supervised
from fastText import load_model
from ai.tools.ticketingsystem import ot as ts


class AiManager(object):
    def __init__(self, mode):
        #mode is either training or exploitation
        self.mode = mode
        self.tool = "ot"
        self.trainingfile = "train.txt"
        self.testfile= "test.txt"
        self.completefile = "data.txt"
        self.epochs=100
        self.learningRate=0.2
        self.wordNgrams=4
        self.ts = ts()
        self.training=False
        if mode =="training":
            self.train()
        else:
            self.model = load_model("/usr/src/app/ai/model.ftz")
    
    

    def getData(self):
        if self.tool == "ot":
            raw =  self.ts.getEmails("all_emails", [ "Subject","Body Plain Text"])
        return raw

    def train(self):
        
        self.training=True
        try:
            self.buildTrainingData()
        except:
            logging.error("failed to build training data")
            self.training=False
        
        
       

        model = train_supervised(input=self.trainingfile, epoch=self.epochs, lr=self.learningRate, wordNgrams=self.wordNgrams, verbose=2, minCount=1)
        self.print_results(*model.test(self.testfile))
        model.save_model("model.bin")
        model.quantize(input=self.trainingfile, qnorm=True, retrain=True, cutoff=100000)
        self.print_results(*model.test(self.testfile))
        model.save_model("model.ftz")
        self.training=False


    def print_results(self, N, p, r):
        print("N\t" + str(N))
        print("P@{}\t{:.3f}".format(1, p))
        print("R@{}\t{:.3f}".format(1, r))

    def buildTrainingData(self):
        #raw should be an array with the fields dict["Title"] dict["Description"] and dict["AssociatedCategory"]
        raw = self.ts.getTrainingData()
        
        ftdata = open('data.txt', 'w')
        logging.error('created file')

        for entry in raw:
            subject = entry['Title']
            body = entry['Description']
            category= entry['AssociatedCategory']
            subject = self.preparedata(subject)
            body = self.preparedata(body)
            txt= f'__label__{category!s} {subject!s} {body!s}'
            ftdata.write(txt)
        ftdata.close()

    def formatdata(self,raw):
        #raw should be a dictionnary with keys dict["Subject"] dict["Body Plain Text"]
        subject = raw['Subject']
        body = raw['Body Plain Text']
        subject = self.preparedata(subject)
        body = self.preparedata(body)
        txt= f'{subject!s} {body!s}'
        return txt
          
    def getCategory(self,text):
        data = self.predict(text)
        try:
            data[0]=ts.getCategoryTitle(data[0])
        except:
            logging.error('getting category failed')

        return data

    def predict(self, text):
        logging.error(f"trying to predict {text!s}")
        logging.error(f"{self.model!s}")
        text=self.preparedata(text)
        prediction = self.model.predict(text, k=2)
        logging.error(f"{prediction!s}")
        cat = prediction[0][0].replace('__label__','')
        confidence = prediction[1][0]
        logging.error(f"{cat!s} / {confidence!s}")
        data = [cat, confidence]
        return data
            
    def preparedata(self, s):
        """
        Given a text, cleans and normalizes it. Feel free to add your own stuff.
        """
        s = s.lower()
        # Replace ips
        s = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ' _ip_ ', s)
        # Isolate punctuation
        s = re.sub(r'([\'\"\.\(\)\!\?\-\\\/\,])', r' \1 ', s)
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
        return s       

    


