This is a complete infrastructure for hosting a fasttext based text classification algorithm, and should be extensible to train other types of models on various data sets.

It's still a bit far from being fully functional. the goal is to be able to test different models quickly, and configure training for various / data structures. Some sample use case will be provided. (email classification, virtual assistant)


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

localhost/api
![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/restapi.png?raw=true)


localhost/tina

![alt text](https://github.com/TheCodingLand/neural-net-ctg/blob/master/tinaaifrontend-wip.png?raw=true)


for example using pre trained vectors :

./fasttext skipgram -input UNLABELED_DATA -output UNSUP_VECTORS

./fasttext supervised -input LABELED_DATA -output MODEL -pretrainedVectors UNSUP_VECTORS.vec
 

I want a block coding interface to chain data exports, splitting, training and prediction based on data.

for this an object will be spawned in the task manager :
 - drawing : name, list of ids blocks (blocks are stored in DB), block instances : [level/hierarchy , links ,  position x/y on the UI]
 - Action : spawn block, link block, run, test
 - Block types : input (json, text, script based), output (text, label/text, image, ...), extract/build data, Train model, Test model, predict model, log, actions (plugin based actions like apis, execute javascript code)

Extract : plugin based : specify type of data input and output (text, label/text, image, sounds, geographic, 3D...)
Predict(model) : input-output is based on a trained model 
Train(model) : input data specified in model, outputs model file
Log: builds logs for elk type data analytics.

