# project/api/views.py
from flask_restplus import Namespace, Resource, fields

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)

from flask import request

from ai.api.restplus import api
from ai.api.models.apimodels import prediction

from ai.ai.aimanager import AiManager

# these hold our data model folder, fields list, required fields
import time


ns = api.namespace('/', description='Ai Api for TINA, virtual agent')
am = AiManager(mode="prediction")

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








@api.response(400, 'failed.')
@ns.route('/train', methods=['GET'])
class Train(Resource):
    @api.response(201, 'train : ok')
    def post(self):
        
        try: 
            d = {} 
            if am.training==False:
                am.train()
                d.update({'training': 'Started !'})
            else:
                d.update({'training': 'Already in progress !'})
           
            if d:
                response_object = {
                    'status': 'success',
                    'message': d
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
@ns.route('/predict', methods=['POST'])
class Prediction(Resource):
    @api.response(201, 'prediction : ok')
    @api.expect(prediction)
    def post(self):

        post_data = request.get_json()
        # log.info(request.get_json())
        try:
            
            
            text = post_data.get('text')
            # predict goes here
            logging.error(text)

            items = am.predict(text)

            logging.error(items)

            d = {}
            d.update({'category': items[0]})
            d.update({'confidence': items[1]})

            d
           

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

