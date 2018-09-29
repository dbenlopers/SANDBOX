FROM alpine:3.7

RUN apk update \
    && apk add gcc g++ musl-dev linux-headers pkgconfig python3 python3-dev \
    && apk add libxml2-dev libxslt-dev libffi-dev openssl-dev \
    && pip3 install apache-airflow
ENV AIRFLOW_HOME /root/airflow
RUN pip3 install cryptography \
    && airflow initdb

CMD ["airflow", "webserver", "-p", "8080"]
