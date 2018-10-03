FROM mariadb:10.1.29

COPY configuration/*				/etc/mysql/conf.d/
COPY init-scripts/*				/docker-entrypoint-initdb.d/
COPY ge-entrypoint.sh				/usr/local/bin/

RUN chmod +x /usr/local/bin/ge-entrypoint.sh

EXPOSE 3306

USER root
ENTRYPOINT ["/usr/local/bin/ge-entrypoint.sh"]
