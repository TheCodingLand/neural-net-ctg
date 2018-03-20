import json

class aimanager(object):
    def __init__(self, config):
        self.modelname = config
        self.config = self.load_config(config)
        #conditional import for ticketing system
        if self.config['tool']=='ot':
            from ai.tools.ticketingsystem import ot as ts
        self.ts = ts()
    
    def load_config(self, config):
        
        configs = json.loads('/trainingdata/config/config.json')
        if config in configs.keys():
            return configs[config]

        return config


    def getData(self):
        jsondata = self.ts.getTrainingData(self.config['filter'], self.config['label'], self.config['fields'])
        #jsondata is just [ { label : "13241", entry :"text"}]
        



        


        
        





