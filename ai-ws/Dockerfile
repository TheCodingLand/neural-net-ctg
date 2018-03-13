FROM python:3.6.1

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



RUN pip install cython

# install requirements
RUN pip install -r requirements.txt

RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR /usr/src/app/fastText
RUN python setup.py install
WORKDIR /usr/src/app
RUN wget https://s3-us-west-1.amazonaws.com/fasttext-vectors/word-vectors-v2/cc.fr.300.bin.gz
RUN gunzip cc.fr.300.bin.gz
# add app
ADD . /usr/src/app/

# run server
CMD python manage.py runserver -h '0.0.0.0'
