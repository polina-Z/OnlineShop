FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Setup Debian linux
RUN export DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y install build-essential curl
RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN node -v && npm -v

# Requirements have to be pulled and installed here, otherwise caching won't work
COPY ./requirements /requirements
COPY package.json /app/

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN npm install -g npm@8.3.0
RUN pip install -r /requirements/local.txt
# RUN npm install && npm run build-development # uncomment this code

COPY ./docker_compose/django/development/start.sh /start.sh
COPY ./docker_compose/django/development/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && sed -i 's/\r//' /start.sh \
    && chmod +x /entrypoint.sh \
    && chmod +x /start.sh

ENTRYPOINT ["/entrypoint.sh"]
