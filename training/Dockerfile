FROM python:latest

RUN apt-get update && apt-get install -y \
        build-essential \
        wget \
        git

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app


RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR /usr/src/app/fastText

RUN make
RUN chmod 777 /usr/src/app/fastText/fasttext

WORKDIR /usr/src/app
RUN pip install --upgrade pip
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

RUN pip install pyfasttext
RUN mkdir -p /trainingdata/textfiles
RUN mkdir -p /trainingdata/models
RUN wget https://drive.google.com/open?id=10FGLZLBqyqYKYqpCrFxIIE9myDOlNm8y -P /trainingdata/models/
ADD data.json /trainingdata/jsonfiles/
ADD . /usr/src/app/
CMD python main.py