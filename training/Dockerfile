FROM python:latest

RUN apt-get update && apt-get install -y \
        build-essential \
        wget \
        git

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD . /usr/src/app/

RUN git clone https://github.com/facebookresearch/fastText.git
WORKDIR /usr/src/app/fastText

RUN make
RUN chmod 777 /usr/src/app/fastText/fasttext

ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

WORKDIR /usr/src/app
CMD python main.py