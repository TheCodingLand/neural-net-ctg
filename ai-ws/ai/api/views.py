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

            results = d
            #for result in items:
            #    d = {}
            #    
            #    results.append(d)

            if results:
                response_object = {
                    'status': 'success',
                    'message': 'object list :',
                    'results': results
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
@ns.route('/train', methods=['POST'])
class Training(Resource):
    @api.response(201, 'prediction : ok')
    @api.expect(prediction)
    def post(self):

        post_data = request.get_json()
        # log.info(request.get_json())
        try:
            log.info(post_data)
            text = post_data.get('text')
            # predict goes here

            items = am.predict(text)

            results = []
            for result in items:
                d = {}
                d.update({'category': result[0]})
                d.update({'confidence': result[1]})
                results.append(d)

            if results:
                response_object = {
                    'status': 'success',
                    'message': 'object list :',
                    'results': results
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