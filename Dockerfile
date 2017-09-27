FROM mrlucascardoso/python-slim-postgres

MAINTAINER Lucas Cardoso <mr.lucascardoso@gmail.com>

ADD ./ /todo_sthima

WORKDIR /todo_sthima

EXPOSE 8000

ENV DEBUG=False

RUN pip install -r requirements.txt