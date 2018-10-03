FROM python:3.6-alpine

RUN apk update \
    && apk add --no-cache --virtual .build-deps git gcc g++ gfortran musl-dev linux-headers libxml2-dev libxslt-dev pkgconfig freetype-dev libpng-dev lapack-dev jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    # Because numpy tries to load it anyway...
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && mkdir /opt
COPY /images/bpmc/config.cfg /images/bpmc/logging.yml /images/bpmc/requirements.txt /images/bpmc/scipy-requirements.txt /opt/sources/configuration/
RUN pip3 --no-cache-dir install -r /opt/sources/configuration/scipy-requirements.txt \
    && pip3 --no-cache-dir install -r /opt/sources/configuration/requirements.txt
COPY /images/bpmc/entrypoint.sh /images/bpmc/db_probe.py /usr/local/bin/
ENV CPT_LOG_CONFIG_FILE /opt/sources/configuration/logging.yml
ENV CPT_CFG_FILE /opt/sources/configuration/config.cfg

ADD ge.bpmc /opt/sources/ge.bpmc
RUN ln -s usr/local/bin/entrypoint.sh / \
    && chmod +x /entrypoint.sh /usr/local/bin/entrypoint.sh /usr/local/bin/db_probe.py \
    && addgroup -S bpm && adduser -S -g bpm bpm \
    && chown -R bpm:bpm /opt/sources /entrypoint.sh /usr/local/bin/entrypoint.sh \
    && cd /opt/sources/ge.bpmc \
    # Building dependencies & pip cache cleanup
    && apk del .build-deps \
    # Those libs are required for packages to run
    && apk update && apk add lapack libstdc++ libxml2 libxslt \
    # Dependencies are already installed, simply linking the module in python modules
    && python setup.py develop

EXPOSE 8080

WORKDIR /opt/sources

USER bpm

ENTRYPOINT ["/entrypoint.sh"]
