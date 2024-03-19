FROM python:3.6-alpine

COPY entrypoint.sh /

RUN apk --no-cache add --virtual=.build-dep build-base \
    && apk --no-cache add libzmq \
    && pip install --no-cache-dir gevent==1.5.0 \
    && pip install --no-cache-dir locustio==0.8.1 \
    && apk del .build-dep \
    && chmod +x /entrypoint.sh

RUN mkdir /locust
WORKDIR /locust
EXPOSE 8089 5557 5558

ENTRYPOINT ["/entrypoint.sh"]
