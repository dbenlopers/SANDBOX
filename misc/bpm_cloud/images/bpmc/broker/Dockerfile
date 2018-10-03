FROM rabbitmq:3.7.3-management-alpine

COPY entrypoint.sh  /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
CMD ["rabbitmq-server"]
