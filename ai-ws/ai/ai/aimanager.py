import json
import os
import requests
import re
from pyfasttext import FastText
import logging
import glob, os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AiManager(object):
    version=1
    modelsFolder = '/trainingdata/models/'
    languageFolder = '/trainingdata/models/'
    languagemodelfile = f'{modelsFolder!s}lid.176.ftz'
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
    epochs = 100
    ngrams = 3
    json=None
    models={}
    defaultlanguage = 'en'
    predictionThreshold = .85
    training=False

    def __init__(self, config, json = None, version = version):
    
        self.modelsFolder=f"{self.modelsFolder!s}{version!s}/"
        try:
            os.mkdir(self.modelsFolder)
        except FileExistsError:
            pass
        self.modelname = config
        
        logger.error(f"loading {self.languagemodelfile!s}")
        self.langdetect = FastText(self.languagemodelfile)
        self.config = self.load_config(config)
        #conditional import for ticketing system
        if self.config['tool']=='ot':
            from ai.tools.ticketingsystem import ot as ts
        self.ts = ts()
        self.load_all_models()
        
    def load_all_models(self):
        """Loads all models in the models folder, and creates a dictionnary {lang:model}"""
        self.models={}
        os.chdir(f"{self.modelsFolder!s}")
        for f in glob.glob("*.bin"):
            lang=f.split('_')[0]
            ftmodel = f"{self.modelsFolder!s}{f!s}"
            self.models.update({lang : FastText(ftmodel)})
        logging.error('finished loading models')
        


    def run_model(self, text, threshold=None):
        """takes text and threshold, returns a label prediction [label,confidence]"""

        if threshold == None:
            threshold=self.predictionThreshold

        lang = self.detectLanguage(text)
        if lang == False:
            lang = self.defaultlanguage
        model = self.models[lang]
        logging.error(lang)

        prediction = model.predict_proba_single(text, k=1)
        logging.error(prediction)
        if prediction:
            if prediction[0][1] > threshold:
                return prediction[0]


    def run_model_multiple(self, text, k=1):
        """builds a list of possible labels, ignores confidence threshold takes text and threshold, returns a label prediction [[label,confidence]]"""

        lang = self.detectLanguage(text)
        logging.error(lang)
        if lang == False:
            lang = self.defaultlanguage
        model = self.models[lang]
        results = []
        
        predictions = model.predict_proba_single(text, k=k)
        logging.error(predictions[0])
        for prediction in predictions:
            if len(prediction) ==2:
                results.append(prediction)
        return results
            
    

    def getLanguageModel(self, language):
        if language in self.models.keys():
            if self.defaultlanguage in self.models.keys():
                language = self.defaultlanguage
            else:
                logging.error('model with specified language not found. Error.')
                return False
        logging.error(language)
        return self.models[language]

    
    def testRun(self, language, threshold, data):
        """this takes a model, and tests it with various paramaters. returns a result dictionnary, 
        {language : "", total : 133, threshold: 85, ignoredEntries : 10, success: 110, failures : 13 }"""
        
    
        model = self.getLanguageModel(language)
        if language==False:
            return False
        

        i = 0
        correct = 0
        percent = 0
        
        for line in data:
            i=i+1
            
            words = line.split()
            label = words[0]
            line = line.replace(label, '')
            #testing only the text, so we remove the label info
            label = label.replace('__label__', '')
            prediction = model.predict_proba_single(line, k=1)
            if prediction[0][1] > threshold:
                if prediction[0][0]==label:
                    correct=correct+1                    
                percent = correct/i*100       
            else:
                i=i-1
        total = len(data)
        ignored = i-total
        failures = total - ignored- correct

        return { "language" : language, "total": total, "success" : correct, "ignored" : ignored, "failures": failures, "percent" : percent }


    def getCategory(self, text):
        """Returns the title of a category instead of the label id"""
        data = self.run_model(text)
        try:
            data[0]=self.ts.getCategoryTitle(data[0])
        except:
            logging.error('getting category failed')

        return data
        
    
    def chat(self, text):

        text = self.preparedata(text)
        filtered = []
        for t in text.split(' '):
            if len(t)>1:
                filtered.append(t)
        text = ' '.join(filtered)
        
        language =self.detectLanguage(text)
        
        model = self.getLanguageModel(language)

        if model == False:
            return False

        try:
            words = model.get_numpy_sentence_vector(text)
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            logging.error(message)
        
        try:
            result = model.words_for_vector(words, k=20)
        
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
        


    def train(self, buildJson=False, loadfile=""):
        """Main function for training a dataset can rebuild a json dataset based on the GetData method, or just prepare the data and train all models"""
        self.training = True
        if loadfile!="":
            try:
                f = open(loadfile, 'r')
                jsonfile = json.load(f)
            except:
                logger.error("failed to load file")
        if buildJson ==True:
            jsonfile = self.getData()
        testresult = []
        self.splitJson(jsonfile)
        print(self.modelname)
        for language in self.languages.keys():
            filename = f'{language!s}_{self.modelname!s}.json'
            f = open(f'{self.jsonFolder!s}{filename!s}', 'r')
            j = json.load(f)
            if len(j['entries']) < 1500:
                f.close()
                continue
            self.splitTrainingData(f'{self.jsonFolder!s}{filename!s}')
            self.createFastText(f'{self.jsonFolder!s}{filename!s}.train')
            self.createFastText(f'{self.jsonFolder!s}{filename!s}.test')
            testfile = f"{self.textfolder!s}{language!s}_{self.modelname!s}.txt.test"
            trainfile = f"{self.textfolder!s}{language!s}_{self.modelname!s}.txt.train"
            print(trainfile)
            modelfile = f"{self.modelsFolder!s}{language!s}_{self.modelname!s}"
            self.startTraining(trainfile, modelfile)
            #testresult.append(self.test(testfile, modelfile))
            testresult.append(self.testRun(language, .85, trainfile))
        self.training = False
        logging.error(testresult)
            

    
    def load_config(self, config):
        """Loads a config files to get the fields and model name to train"""
        f=open(f'{self.configFolder!s}config.json' ,'r')
        configs = json.load(f)
        if config in configs.keys():
            return configs[config]

        return config

    def detectLanguage(self, text):
        """Detects language, or returns defaultLanguage, as a 2 letters laguage identifier"""
        lang = self.langdetect.predict_proba_single(text,k=1)
        logging.error(lang)
        # we only need to return the first language and probability should be useless at this point.
        # could be used later to default to english ??
        try:
            lang = lang[0][0]
        except:
            lang = self.defaultlanguage
        #keeping track on all languages used
        return lang

    def splitJson(self, jsondata):
        """Split json data into separate languge files"""

        for entry in jsondata['entries']:
            lang = self.detectLanguage(entry['text'])
            if lang not in self.languages.keys():
                f = open(f'{self.jsonFolder!s}{lang!s}_{self.modelname!s}.json', 'w')
                self.languages.update({ lang: { "data" : {'entries': []}, "file":f}})


            self.languages[lang]['data']['entries'].append(entry)
            
        
        for lang in self.languages.keys():
            #print (self.languages[lang]['data'])
            json.dump(self.languages[lang]['data'],self.languages[lang]['file'])
            self.languages[lang]['file'].close()
        
    
    def splitTrainingData(self, jsonfile):
        """Split data in two based on ratio, training and testing files"""

        trainjf = open(f"{jsonfile!s}.train",'w')
        testjf = open(f"{jsonfile!s}.test",'w')
        with open(jsonfile) as f:
            jf = json.load(f)
            count = len(jf['entries'])
        
            breakpoint = int(count * self.ratio /100)
            print (breakpoint)
            train = { "entries": jf['entries'][0:breakpoint]}
            test = { "entries": jf['entries'][breakpoint:-1]}


            
            json.dump(train,trainjf)
            json.dump(test,testjf)
            trainjf.close()
            testjf.close()

        
    def createFastText(self, jsonfile):
        """Creates Fasttext Based syntax files for supervised training : __label__category text
        Takes Json file as input"""
        
        textfile =jsonfile.split('/')[-1].replace('.json','.txt')
        with open(f'{self.textfolder}{textfile!s}', 'w') as f:
            jsfile = open(f'{jsonfile!s}')
            for entry in json.load(jsfile)['entries']:
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
        """Gets data as a main data dump into usable form by the rest of the program to build """
        jsondata = self.ts.getTrainingData(self.config['filter'], self.config['label'], self.config['fields'])
        #jsondata is just [ { label : "13241", entry :"text"}]
        return jsondata
    
    def removeShort(self, text):
        """ I got better result with removing words of less than 2 characters, need to play around with this more, maybe filter out only other than [aA-zZ]"""
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
        This really improves prediction by a lot.
        Specific applications might not want to remove numbers for example though
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

    def startTraining(self, trainingfile, modelfile):
        """Starts model building"""
        
        if self.reBuildModel==True:
            logger.info(f'Training started with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.ngrams!s}')
            model = FastText()
     
            model.supervised(input=trainingfile, output=modelfile, epoch=self.epochs, lr=self.learningRate, wordNgrams=self.ngrams, verbose=2, minCount=1)
            logger.error(f'finished training model with : learningRate:{self.learningRate!s}, epochs:{self.epochs!s}, ngrams :{self.ngrams!s}')

            
           

    def test(self, testfile, modelfilename, threshold=None):
        """Takes a testfile in fasttext format, and a modelfile, and checks if we can successfully predict the label"""
        
        logger.error(f'testing {modelfilename!s}')
        
        if threshold ==None:
            threshold = self.predictionThreshold

        model= FastText(f'{modelfilename!s}.bin')
        i=0
        correct=0
        
        with open(testfile) as f:
            lines = f.readlines()
            percent = 0
            for line in lines:
                i=i+1
                
                words = line.split()
                label = words[0]
                line = line.replace(label, '')
                #testing only the text, so we remove the label info
                label = label.replace('__label__', '')
                prediction = model.predict_proba_single(line, k=1)
   
                if prediction[0][1] > threshold:
                    if prediction[0][0]==label:
                        
                        correct=correct+1
                        
                    percent = correct/i*100       
                else:
                    i=i-1
                


            logging.error(f"results : {correct!s}/{i!s}, {percent!s}%")
            return [modelfilename, correct, i, percent]

#api = AiManager('ot_emails')
#api.train(buildJson=False,loadfile='/trainingdata/jsonfiles/data2.json')

#data = api.getData()
#f = open(f'{api.modelname!s}.json','w')


        
        





