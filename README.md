This is a complete infrastructure for hosting a fasttext based text classification algorithm.

Progress can be seen at http://julien.tech:5011

API at http://julien.tech:5005/api

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/architecture.png?raw=true)

The infrastructure is very basic and meant for a proof of concept.

instructions : 

git clone https://github.com/TheCodingLand/neural-net-ctg.git

cd neural-net-ctg

docker-compose up

Currently the ports are all over the place as the reverse proxy/load balancer is not yet configured.

localhost:5102 for swagger
localhost:5005 for the rest api

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/restapi.png?raw=true)



localhost:5011 for the ai front end

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/tinaaifrontend-wip.png?raw=true)

Done : 
API :
- api calls to the fasttext AI
- returning predicted category based on loaded models
- implement the possibility to support several ticketing backends for data importing.

AI:
- make it possible to start in predicting mode, or in training mode
- added sample trained model

Frontend : 
- basic ui frontend with CTG colors and material ui
- conversation with bot saved to localStorage of the browser
- Redux implementation for state management and future developments

TODO :

Frontend : 
- Glue api to frontend
- uploads of data, training mode
- model selection


API:
- model selection
- return meaningful data for the client instead of labels and confidence

AI:
- model selection
 

