FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -yq curl git nano

RUN apt-get install -y npm
RUN npm install -g npm

RUN curl -sL https://deb.nodesource.com/setup_9.x | bash -

RUN apt-get install -y nodejs

RUN npm install -g http-server

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ADD . /usr/src/app

RUN npm install
RUN npm run build

#RUN mkdir -p /usr/app/tina
RUN mkdir -p /usr/app/tina/tina

RUN yes | cp -rf /usr/src/app/build/* /usr/app/tina/tina

WORKDIR /usr/app/tina/tina
#CMD ["npm", "start"]

CMD ["http-server"]