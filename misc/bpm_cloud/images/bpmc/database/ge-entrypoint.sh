#!/bin/bash

if [ -z $MYSQL_ROOT_PASSWORD ] && [ -z $MYSQL_ROOT_PASSWORD_FILE ] && [ -f $APP_ADB_ROOT_PASSWORD_FILE ]; then
	export MYSQL_ROOT_PASSWORD=$(cat $APP_ADB_ROOT_PASSWORD_FILE)
fi

if [ -z $APP_DATABASE_PASSWORD ] && [ -f $APP_DATABASE_PASSWORD_FILE ]; then
	export APP_DATABASE_PASSWORD=$(cat $APP_DATABASE_PASSWORD_FILE)
fi

if [ -z $APP_DATABASE_PASSWORD ]; then
	echo >&2 'error: database password option(s) is/are not specified '
    echo >&2 ' You need to specify one of $APP_DATABASE_PASSWORD or $APP_DATABASE_PASSWORD_FILE '
    exit 1
fi

if [ -z $CPT_INNODB_BUFFER_POOL_SIZE ]; then
	CPT_INNODB_BUFFER_POOL_SIZE="2G"
fi

# Update datawatch db initialization files

sed -i 's~$APP_DATABASE_PASSWORD~'"$APP_DATABASE_PASSWORD"'~g'    /docker-entrypoint-initdb.d/bpmc-init.sql
sed -i 's~$INNODB_BUFFER_POOL_SIZE~'"$CPT_INNODB_BUFFER_POOL_SIZE"'~g'  /etc/mysql/conf.d/bpmc.cnf 

# back to the original init script

echo "Variables set, called docker entrypoint with command $1"
echo "INNODB BUFFER POOL SIZE: $CPT_INNODB_BUFFER_POOL_SIZE"
source /docker-entrypoint.sh mysqld