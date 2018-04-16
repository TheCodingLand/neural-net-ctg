# project/api/views.py
from flask_restplus import Namespace, Resource, fields

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

from flask import request
import recastai
RECAST_TOKEN="78ceb95a23a923c4b6fd1afbde85ac85"
from ai.api.restplus import api
from ai.api.models.apimodels import prediction, training, model

from ai.ai.aimanager import Config

# these hold our data model folder, fields list, required fields
import time


ns = api.namespace('/', description='Ai Api for TINA, virtual agent')

class ModelDefinition(object):
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.config = Config(name)
    def load(self):
        self.config.ai.load_all_models()






tm = ModelDefinition('ot_tickets_solutions')
um = ModelDefinition('ot_solutions')
am = ModelDefinition('ot_emails')
#am.load()
#um.load()
models = [am, um, tm]


@ns.route('/schema')
class Swagger(Resource):
    def get(self):
        return api.__schema__


@ns.route('/ping')
class SanityCheck(Resource):
    def get(self):
        # log.info(json.dumps(api.__schema__))
        return {
            'status': 'success',
            'message': 'pong!'
        }


@ns.route('/train', methods=['POST'])
class Train(Resource):
    @api.response(201, 'train : ok')
    @api.expect(training)
    def post(self):
        d = {} 
        post_data = request.get_json()
        config = post_data.get('config')
        for conf in models:
            if conf.name == config:
                if conf.config.ai.training==False:
                    conf.config.ai.train(buildJson=True,loadfile="")
                    d.update({'training': 'Started !'})
                else:
                    d.update({'training': 'Already in progress !'})

        try: 
            #check if training is already in progress
            

            if d:
                response_object = {
                    'status': 'success',
                    'message': d
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Training Failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'server error.'
            }
            return response_object, 500




@api.response(400, 'failed.')
@ns.route('/loadmodel', methods=['POST'])
class loadmodel(Resource):
    @api.response(201, 'loaded')
    @api.expect(model)
    def post(self):

        post_data = request.get_json()
        model = post_data.get('model')
        am = ModelDefinition(model)
        am.load()
        logging.error(model)
        try:      
            response_object = {
                    'status': 'success',
                    'model' : model
                }
            return response_object, 201

        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400


@api.response(400, 'failed.')
@ns.route('/predict', methods=['POST'])
class Prediction(Resource):
    @api.response(201, 'prediction : ok')
    @api.expect(prediction)
    def post(self):

        post_data = request.get_json()
        text = post_data.get('text')
            # predict goes here
        logging.error(text)

        items = am.config.ai.run_model(text,.5)
        # log.info(request.get_json())
        try:
            
            #here we will establish a context for the bot to talk into
            #user can guide the bot into several contexts. context will be displayed. 
            # starting with small talk

            logging.error(items)
            d = {}
            d.update({'label': items[0]})
            d.update({'confidence': items[1]})
            if d:
                response_object = {
                    'status': 'success',
                    'results': d
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400

@api.response(400, 'failed.')
@ns.route('/chat', methods=['POST'])
class Chat(Resource):
    @api.response(201, 'prediction : ok')
    @api.expect(prediction)
    def post(self):

        post_data = request.get_json()
        # log.info(request.get_json())
        try:
            
            
            text = post_data.get('text')
            # predict goes here
            logging.error(text)
            #here we will establish a context for the bot to talk into
            #user can guide the bot into several contexts. context will be displayed. 
            # starting with small talk
            build = recastai.Build(RECAST_TOKEN, 'en')
            response = build.dialog({'type': 'text', 'content': text }, 'CONVERSATION_ID')
            
            logging.error(f'{dir(response)!s}')

            
            logging.error(f'{dir(response.messages)}')
            d = {}
            try:
                txt = response.messages[0].content
            except:
                txt = "I think I\'m getting it. keep talking to me :)"
            d.update({'response': txt})

            if d:
                response_object = {
                    'status': 'success',
                    'results': d,
                    
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400




@api.response(400, 'failed.')
@ns.route('/categorize', methods=['POST'])
class getCategory(Resource):
    @api.response(201, 'prediction : ok')
    @api.expect(prediction)
    def post(self):

        post_data = request.get_json()
        # log.info(request.get_json())
        try:
            text = post_data.get('text')
            # predict goes here
            logging.error(text)
            items = am.config.ai.getCategory(text)
            
            #here we will establish a context for the bot to talk into
            #user can guide the bot into several contexts. context will be displayed. 
            # starting with small talk
            logging.error(items)
            d = {}
            d.update({'label': items[0]})
            d.update({'confidence': items[1]})
            if d:
                response_object = {
                    'status': 'success',
                    'results': d
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400


@api.response(400, 'failed.')
@ns.route('/updatebrain', methods=['POST'])
class UpdateBrain(Resource):
    @api.response(201, 'prediction : ok')
    @api.expect(prediction)
    def post(self):

        post_data = request.get_json()
        text = post_data.get('text')

        
        logging.error(text)
        items = am.config.ai.run_model_multiple(text,5)
        i=0
        logging.error(items)
        results = []
        # log.info(request.get_json())
        try:
            
            for item in items:
                d={}
                i=i+1
                d.update({"id":i , "label":item[0], "confidence":item[1]})

                results.append(d)
            
            
            #testing
            words = am.config.ai.chat(text)
            #here we will establish a context for the bot to talk into
            #user can guide the bot into several contexts. context will be displayed. 
            # starting with small talk

            logging.error(results)
            
            if items:
                response_object = {
                    'status': 'success',
                    'results': results,
                    'words' : words
                }
                return response_object, 201
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'Sorry. failed.'
                }
                return response_object, 400
        except:
            response_object = {
                'status': 'fail',
                'message': 'Invalid payload.'
            }
            return response_object, 400