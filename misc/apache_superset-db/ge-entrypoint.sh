#!/bin/bash

if [ -z $MYSQL_ROOT_PASSWORD ] && [ -z $MYSQL_ROOT_PASSWORD_FILE ] && [ -f $APP_ROOT_PASSWORD_FILE ]; then
	export MYSQL_ROOT_PASSWORD=$(cat $APP_ROOT_PASSWORD_FILE)
fi

if [ -z $APP_SUPERSET_PASSWORD ] && [ -f $APP_SUPERSET_PASSWORD_FILE ]; then
	export APP_SUPERSET_PASSWORD=$(cat $APP_SUPERSET_PASSWORD_FILE)
fi

if [ -z $APP_SUPERSET_PASSWORD ]; then
	echo >&2 'error: database in unitialized and password option(s) is/are not specified '
        echo >&2 ' You need to specify one of $APP_SUPERSET_PASSWORD or $APP_SUPERSET_PASSWORD_FILE '
	exit 1
fi

if [ -z $APP_INNODB_BUFFER_POOL_SIZE ]; then
	APP_INNODB_BUFFER_POOL_SIZE="2G"
fi

# Update datawatch db initialization files

sed -i 's~$APP_SUPERSET_PASSWORD~'"$APP_SUPERSET_PASSWORD"'~g'			/docker-entrypoint-initdb.d/superset-init.sql
sed -i 's~$INNODB_BUFFER_POOL_SIZE~'"$APP_INNODB_BUFFER_POOL_SIZE"'~g'		/etc/mysql/conf.d/superset.cnf 

# back to the original init script

echo "INNODB BUFFER POOL SIZE: $APP_INNODB_BUFFER_POOL_SIZE"
source /docker-entrypoint.sh mysqld
