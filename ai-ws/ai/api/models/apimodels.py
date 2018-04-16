
from flask_restplus import fields
from ai.api.restplus import api


prediction = api.model('prediction:', {
    'text': fields.String(description='text to feed the prediction algorithm'),
    
})

model = api.model('model:', {
    'text': fields.String(description='name of the model to laod'),
    
})



training = api.model('training:', {
    'config': fields.String(description='name of the configuration model'),
    
})
