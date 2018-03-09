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

# add app
ADD . /usr/src/app/

# run server
CMD python manage.py runserver -h '0.0.0.0'
