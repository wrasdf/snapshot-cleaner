FROM python:alpine3.7
WORKDIR /app

RUN apk --update add gcc make bash jq curl postgresql-dev musl-dev && \
  rm -rf /tmp/* /var/cache/apk/*

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
