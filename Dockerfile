
FROM python:3.8.10-alpine
RUN apk update && apk upgrade
RUN apk add --no-cache bash
RUN apk add  --no-cache bash gcc
RUN apk add  --no-cache bash openldap
RUN apk add  --no-cache bash libcurl
RUN apk add  --no-cache bash python3-dev


RUN rm -rf /var/cache/apk/*
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1

COPY . .
RUN pip install  --upgrade setuptools
RUN python -m pip install --upgrade pip
RUN pip install --upgrade wheel

COPY requirements-base.txt requirements-base.txt
RUN pip install  --no-cache-dir -r requirements-base.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN pip install  -e .
WORKDIR /app/
ENV MODULE_NAME=fast_bloge.main
CMD ["./start.sh"]
