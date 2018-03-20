This is a complete infrastructure for hosting a fasttext based text classification algorithm.
Part rewrite of training api is in progress, refactoring training using settings file, and changing trigger mecanism
The system is sitting behind a traefik reverse load balancer.

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/architecture.png?raw=true)

Trello : 
https://trello.com/b/SmrexYcg/ai-project

The infrastructure is very basic and meant for a proof of concept.

instructions : 

git clone https://github.com/TheCodingLand/neural-net-ctg.git

cd neural-net-ctg

docker-compose up

possible to scale up using :
docker-compose <service> scale=x


localhost:10000/ : dashboard for load balancer.

localhost:9999/api

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/restapi.png?raw=true)


localhost:9999/tina

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/tinaaifrontend-wip.png?raw=true)


Progress: it's now thinking about possible issues, notifying users of the progress of finding a solution : 
![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/brain.png?raw=true)



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

- link models together using another AI.
- demonstrate https, webhooks


Frontend :
- uploads of data, training mode
- model selection
- brain visualization


API:
- HTTPS implementation for webhook support
- model selection
- return meaningful data for the client instead of labels and confidence


AI:
- model selection
- pre train model using skipgram on other unclassified data

for example using pre trained vectors :

./fasttext skipgram -input UNLABELED_DATA -output UNSUP_VECTORS

./fasttext supervised -input LABELED_DATA -output MODEL -pretrainedVectors UNSUP_VECTORS.vec
 

