This is a complete infrastructure for hosting a fasttext based text classification algorithm, and should be extensible to train other types of models on various data sets.

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


for example using pre trained vectors :

./fasttext skipgram -input UNLABELED_DATA -output UNSUP_VECTORS

./fasttext supervised -input LABELED_DATA -output MODEL -pretrainedVectors UNSUP_VECTORS.vec
 

