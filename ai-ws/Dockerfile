FROM python:latest

# set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add requirements (to leverage Docker cache)
ADD ./requirements.txt /usr/src/app/requirements.txt

#Dependencies for building Fasttext
RUN apt-get update && apt-get install -y \
        build-essential \
        wget \
        git


# install requirements
RUN pip install -r requirements.txt

RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR /usr/src/app/fastText
RUN python setup.py install
WORKDIR /usr/src/app
#RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/word-vectors-v2/cc.fr.300.bin.gz
#RUN gunzip cc.fr.300.bin.gz
# add app

WORKDIR /usr/src/app/fastText

RUN make
RUN chmod 777 /usr/src/app/fastText/fasttext
WORKDIR /usr/src/app
RUN pip install -r requirements.txt
RUN pip install pyfasttext

RUN mkdir -p /trainingdata/textfiles
RUN mkdir -p /trainingdata/models
RUN mkdir -p /trainingdata/jsonfiles
RUN mkdir -p /trainingdata/config

ADD ./config.json /trainingdata/config/config.json

WORKDIR /trainingdata/models
RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/supervised_models/lid.176.ftz -O /trainingdata/models/lid.176.ftz
WORKDIR /usr/src/app
# run server
ADD . /usr/src/app/
CMD python manage.py runserver -h '0.0.0.0'
