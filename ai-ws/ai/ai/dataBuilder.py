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

        raw = self.tool.getTrainingData()

        ftdata = open('.txt', 'w')
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
        
        return raw