import logging
from ai.tools.ticketingsystem import ot


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



 
 
class dataBuilder(object):

    supportedTools = {'ot': ot() , 'me' : ot()}
    model = None

    def __init__(self, model='data', tool=None, labelField=None):
        if tool not in self.supportedTools.keys():
            logging.error(f"we do not support this tool yet : {tool!s}")
            exit()
        #looks like a cool way to load classes conditionnaly
        self.tool = self.supportedTools[tool]
        self.model = model
        self.getData()

        
         
    def getData(self):
        
        fields = ["Title","Description"]
        
        raw = self.tool.getTrainingData(self.model,)
        
        result = { 'model' : model, 'labelfield' : labelfield, 'entries' : entries }
        model = raw['model']


        for entry in raw['entries']:
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
         
        
        return raw

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
    
    def removeShort(self, text):
        t = text.split(' ')
        result= []
        for s in t:
            if len(s)>1:
                result.append(s)
        
        result = ' '.join(result)
        return result