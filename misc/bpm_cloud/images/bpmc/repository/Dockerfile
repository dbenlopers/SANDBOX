FROM alpine:3.7

LABEL maintainer="NGINX Docker Maintainers <docker-maint@nginx.com> updated by General Electrics <julien.stegle@ge.com>"

ENV NGINX_VERSION 1.12.2
ENV WEBDAV_EXT_VERSION 0.1.0

RUN CONFIG="\
		--prefix=/etc/nginx \
		--sbin-path=/usr/sbin/nginx \
		--modules-path=/usr/lib/nginx/modules \
		--conf-path=/etc/nginx/nginx.conf \
		--error-log-path=/var/log/nginx/error.log \
		--http-log-path=/var/log/nginx/access.log \
		--pid-path=/var/run/nginx.pid \
		--lock-path=/var/run/nginx.lock \
		--user=nginx \
		--group=nginx \
		--with-http_ssl_module \
		--with-http_dav_module \
        --add-module=/nginx-dav-ext-module-$WEBDAV_EXT_VERSION \
	" \
	&& addgroup -S nginx \
	&& adduser -D -S -h /var/cache/nginx -s /sbin/nologin -G nginx nginx \
	&& apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		make \
		openssl-dev \
		pcre-dev \
		zlib-dev \
		linux-headers \
		curl \
		gnupg \
		libxslt-dev \
		gd-dev \
		geoip-dev \
        expat-dev \
    && curl -kfSL https://github.com/arut/nginx-dav-ext-module/archive/v$WEBDAV_EXT_VERSION.zip -o nginx-dav-ext-module.zip \
    && unzip nginx-dav-ext-module.zip \
	&& curl -kfSL https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz -o nginx.tar.gz \
	&& curl -kfSL https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz.asc  -o nginx.tar.gz.asc \
	&& mkdir -p /usr/src \
	&& tar -zxC /usr/src -f nginx.tar.gz \
    && rm nginx.tar.gz \
	&& cd /usr/src/nginx-$NGINX_VERSION \
	&& ./configure $CONFIG --with-debug \
	&& make -j$(getconf _NPROCESSORS_ONLN) \
	&& mv objs/nginx objs/nginx-debug \
	&& ./configure $CONFIG \
	&& make -j$(getconf _NPROCESSORS_ONLN) \
	&& make install \
	&& rm -rf /etc/nginx/html/ \
	&& mkdir /etc/nginx/conf.d/ \
	&& mkdir -p /usr/share/nginx/html/ \
	&& install -m644 html/index.html /usr/share/nginx/html/ \
	&& install -m644 html/50x.html /usr/share/nginx/html/ \
	&& install -m755 objs/nginx-debug /usr/sbin/nginx-debug \
	&& ln -s ../../usr/lib/nginx/modules /etc/nginx/modules \
	&& strip /usr/sbin/nginx* \
	&& rm -rf /usr/src/nginx-$NGINX_VERSION \
	\
	# Bring in gettext so we can get `envsubst`, then throw
	# the rest away. To do this, we need to install `gettext`
	# then move `envsubst` out of the way so `gettext` can
	# be deleted completely, then move `envsubst` back.
	&& apk add --no-cache --virtual .gettext gettext \
	&& mv /usr/bin/envsubst /tmp/ \
	\
	&& runDeps="$( \
		scanelf --needed --nobanner --format '%n#p' /usr/sbin/nginx /usr/lib/nginx/modules/*.so /tmp/envsubst \
			| tr ',' '\n' \
			| sort -u \
			| awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
	)" \
	&& apk add --no-cache --virtual .nginx-rundeps $runDeps \
	&& apk del .build-deps \
	&& apk del .gettext \
	&& mv /tmp/envsubst /usr/local/bin/ \
	\
	# Bring in tzdata so users could set the timezones through the environment
	# variables
	&& apk add --no-cache tzdata \
	\
	# forward request and error logs to docker log collector
	&& ln -sf /dev/stdout /var/log/nginx/access.log \
	&& ln -sf /dev/stderr /var/log/nginx/error.log

COPY nginx.conf /etc/nginx/nginx.conf
COPY webdav.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /usr/local/bin/
COPY service-registry.json /

RUN apk add --no-cache openssl curl
RUN ln -s usr/local/bin/entrypoint.sh / \
    && chmod +x /entrypoint.sh /usr/local/bin/entrypoint.sh \
    && mkdir -p /var/www/webdav/files \
    && mkdir -p /var/www/webdav/temp \
    && chown -R nginx:nginx /var/www/webdav /entrypoint.sh /usr/local/bin/entrypoint.sh /service-registry.json

EXPOSE 80

STOPSIGNAL SIGTERM

ENTRYPOINT ["/entrypoint.sh"]