

# there will be 2 or more models used by the bot. 
# the binary pre trained vectors will deduce context better than commercialy available chat bot solutions
# we will still use them for recognizing data types that are not "words"
# then a business classified model will be used to extract very specific business information.False


#the bin model will be accessible with the chat method and /chat api endpoint
#while the predict method will return business specific information on the /predict api endpoint
#business data has to be formated into :
# __label__category and a sentence that should be assigned to it \n
#another format possible :
#__label__category1 __label__category2 a sentence that should be assigned to both categories
#can be extended to support other ticketing systems later
# and be trained

import logging
import re
import os
import subprocess
from fastText import train_supervised
from fastText import load_model
from fastText.util import find_nearest_neighbor
from ai.tools.ticketingsystem import ot as ts
from pyfasttext import FastText

class AiManager(object):
    def __init__(self, mode):
        #mode is either training or exploitation
        self.mode = mode
        self.tool = "ot"
        self.trainfile=""
        self.testfile=""
        self.trainingname=""
        self.epochs=100
        self.learningRate=0.2
        self.wordNgrams=3
        self.ts = ts()
        self.training=False
        
        self.rebuildData=False
    
    def load_model(self):



        self.model = FastText("/trainingdata/models/en_data.bin")
        self.unsupModel = FastText("/trainingdata/models/en_data.bin")
            

    def chat(self, text):
        text = self.preparedata(text)
        filtered = []
        for t in text.split(' '):
            if len(t)>5:
                filtered.append(t)
        text = ' '.join(filtered)

  

        try:
            words = self.unsupModel.get_numpy_sentence_vector(text)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
        
        #logging.error(dir(words))

        try:
            result = self.unsupModel.words_for_vector(words, k=20)
        
        # try:
        #     nearest = find_nearest_neighbor(words)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)

        logging.error(result)

        results =[]
      
        i=0
        for w in result:
            d= {}
            
            d.update({"id":i})
            d.update({"word":w[0]})
            d.update({"confidence":w[1]})
            i=i+1
            results.append(d)
        logging.error(results)
        return results

       



    def getData(self):
        if self.tool == "ot":
            raw =  self.ts.getEmails("all_emails", [ "Subject","Body Plain Text"])
        return raw

    def train(self):
        
        self.training=True
        if self.rebuildData ==True:
            try:
                self.buildTrainingData()
            except:
                logging.error("failed to build training data")
                self.training=False

        logging.error(f'Training started with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')

        model = train_supervised(input=self.completefile, epoch=200, lr=0.2, wordNgrams=self.wordNgrams, verbose=2, minCount=1)
        #self.print_results(*model.test(self.completefile))
        logging.error(f'finished training model with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.wordNgrams!s}')
        model.save_model("model.bin")
        model.quantize(input=self.completefile, qnorm=True, retrain=True, cutoff=100000)
        self.print_results(*model.test(self.completefile))
        model.save_model("model.ftz")
        self.training=False
        return self.training


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
            #logging.error(entry)
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
        cat2 = prediction[0][1].replace('__label__','')
        confidence = prediction[1][0]
        logging.error(f"{cat!s} / {confidence!s}")
        data = [cat, confidence, cat2]
        return data
    
    def removeShort(self, text):
        t = text.split(' ')
        result= []
        for s in t:
            if len(s)>2:
                result.append(s)
        
        result = ' '.join(result)
        return result


    def updatebrain(self, text):
        logging.error(f"trying to predict {text!s}")
        logging.error(f"{self.model!s}")
        text=self.preparedata(text)
        prediction = self.model.predict(text, k=5)
        logging.error(f"{prediction!s}")
        results =[]
      
        i=0
        for cat in prediction[0]:
            d= {}
            catid = cat.replace('__label__','')
            logging.error(catid)
            
            #cattitle=self.ts.getCategoryTitle(catid)
            cattitle = catid
            logging.error(cattitle)
            
            d.update({"id":i})
            d.update({"category":cattitle})
            d.update({"confidence":prediction[1][i]})
            i=i+1
            results.append(d)
        return results
            
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

        return s       

    


