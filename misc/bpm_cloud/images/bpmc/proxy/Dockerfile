FROM nginx:1.12.2-alpine

# openssl req -nodes -new -x509 -keyout proxy_https.key -out proxy_https.crt -days 1800
# Country Name (2 letter code) [AU]:FR
# State or Province Name (full name) [Some-State]:Alsace
# Locality Name (eg, city) []:Strasbourg
# Organization Name (eg, company) [Internet Widgits Pty Ltd]:GE Healthcare
# Organizational Unit Name (eg, section) []:PH8
# Common Name (e.g. server FQDN or YOUR name) []:ge.bpmc
# Email Address []:julien.stegle@ge.com

COPY ssl/   /etc/ssl/certs/
COPY bpmc.conf /etc/nginx/conf.d/default.conf
COPY entrypoint.sh /usr/local/bin/

RUN chmod +x /usr/local/bin/entrypoint.sh \
    && ln -s /usr/local/bin/entrypoint.sh / \
    && chown -R nginx:nginx /etc/ssl/certs/ /etc/nginx/conf.d/ /usr/local/bin/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]