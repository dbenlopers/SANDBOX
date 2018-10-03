FROM python:3.4.7-alpine

ENV SUPERSET_VERSION="0.25.6"

RUN apk update && \
    mkdir -p /opt/superset && \
    apk add gcc g++ gfortran make libffi-dev cyrus-sasl-dev openssl-dev openssl

COPY extra_requirements.txt	/opt/superset_requirements/extra_requirements.txt

RUN pip install -r /opt/superset_requirements/extra_requirements.txt
RUN pip install superset=="$SUPERSET_VERSION"

COPY superset_config.py 		/opt/superset
COPY entrypoint.sh      		/usr/local/bin/entrypoint.sh
COPY templates				/opt/superset_templates
COPY probes				/opt/superset_probes

RUN adduser -S superset && \
    chmod +x /usr/local/bin/entrypoint.sh && \
    chown -R superset:nogroup /usr/local/bin/entrypoint.sh /opt/superset /opt/superset_templates /opt/superset_probes

ENV PYTHONPATH=/opt/superset

EXPOSE 8088

USER superset

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

