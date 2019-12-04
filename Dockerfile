FROM python:3.8-alpine3.10
WORKDIR /app

RUN apk --update add gcc musl-dev libffi-dev python3-dev openssl-dev make bash jq curl && \
  rm -rf /tmp/* /var/cache/apk/*

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt
