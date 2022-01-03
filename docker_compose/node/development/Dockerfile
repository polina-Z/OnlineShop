FROM node:16

COPY . /app

WORKDIR /app
RUN npm install -g npm@8.3.0

COPY ./docker_compose/node/development/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh
RUN chmod +x /start.sh
