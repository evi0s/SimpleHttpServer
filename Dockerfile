FROM python

MAINTAINER evi0s <wc810267705@163.com>

RUN mkdir /app

ADD . /app

WORKDIR /app

EXPOSE 80

CMD python3 app.py
