
from flask_restplus import fields
from ai.api.restplus import api


prediction = api.model('prediction:', {
    'text': fields.String(description='text to feed the prediction algorithm'),
    
})



