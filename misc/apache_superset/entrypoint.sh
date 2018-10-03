#!/bin/sh

APP_ADMIN_USER=${APP_ADMIN_USER:-admin}
APP_ADMIN_USER_FN=${APP_ADMIN_USER_FN:-admin}
APP_ADMIN_USER_LN=${APP_ADMIN_USER_LN:-admin}
APP_ADMIN_USER_EMAIL=${APP_ADMIN_USER_EMAIL:-admin_superset@ge.com}
APP_CACHE_TYPE=${APP_CACHE_TYPE:-none}
APP_BROKER_TYPE=${APP_BROKER_TYPE:-none}
APP_USE_LOCAL_DB=${APP_USE_LOCAL_DB:-false}
APP_SUPERSET_MODE=${APP_SUPERSET_MODE:-default}
APP_SECRET_KEY=${APP_SECRET_KEY:-LCcgJCzHbp1LM1TTg+m0n8sb2iPYhk4flg==}
APP_TIMEOUT=${APP_TIMEOUT:-300}

if [ -z "$APP_ADMIN_USER_PASSWORD_FILE" ]; then
	APP_ADMIN_USER_PASSWORD_FILE=/etc/missing
fi

if [ -z "$APP_ADMIN_USER_PASSWORD" ] && [ -f "$APP_ADMIN_USER_PASSWORD_FILE" ]; then
	APP_ADMIN_USER_PASSWORD=$(cat $APP_ADMIN_USER_PASSWORD_FILE)
fi

if [ -z "$APP_DB_PASSWORD" ] && [ -f "$APP_DB_PASSWORD_FILE" ]; then
        APP_DB_PASSWORD=$(cat $APP_DB_PASSWORD_FILE)
fi

if [ -z "$APP_CACHE_PASSWORD" ] && [ -f "$APP_CACHE_PASSWORD_FILE" ]; then
        APP_CACHE_PASSWORD=$(cat $APP_CACHE_PASSWORD_FILE)
fi

if [ -f "$APP_SECRET_KEY_FILE" ]; then
	APP_SECRET_KEY=$(cat $APP_SECRET_KEY_FILE)
fi

# Timeout mngmt

NUMBER='^[0-9]+$'
case $APP_TIMEOUT in
    ''|*[!0-9]*) echo >&2 '$APP_TIMEOUT is not a number'; echo >&2 'Please correct your configuration.'; exit 1 ;;
    *) ;;
esac

# Cache management

AVAILABLE_CACHE_TYPES='redis none'
APP_CACHE_TYPE_VALID=`echo $AVAILABLE_CACHE_TYPES | grep $APP_CACHE_TYPE | wc -l`
if [ "$APP_CACHE_TYPE_VALID" -eq 0 ]; then
	echo >&2 'Specified cache type is invalid: $APP_CACHE_TYPE;'
	echo >&2 'support cache types: $AVAILABLE_CACHE_TYPES'
	exit 1
fi

if [ "$APP_CACHE_TYPE" != 'none' ] && { [ -z "$APP_CACHE_HOST" ] || [ -z "$APP_CACHE_PORT" ]; }; then
	echo >&2 'You have specified a cache type, please set following environment variables'
	echo >&2 'APP_CACHE_HOST, APP_CACHE_PORT, APP_CACHE_LOGIN and APP_CACHE_PASSWORD. If no auth is required, ignore LOGIN & PASSWORD'
	exit 1
fi

if [ -z "$APP_CACHE_LOGIN" ] && [ -z "$APP_CACHE_PASSWORD" ]; then
	APP_CACHE_AUTH=""
else
	APP_CACHE_AUTH="$APP_CACHE_LOGIN:$APP_CACHE_PASSWORD@"
fi

# Mode management

AVAILABLE_MODES='default worker'
APP_SUPERSET_MODE_VALID=`echo $AVAILABLE_MODES | grep $APP_SUPERSET_MODE | wc -l`
if [ "$APP_SUPERSET_MODE_VALID" -eq 0 ]; then
        echo >&2 'Specified mode type is invalid: $APP_SUPERSET_MODE;'
        echo >&2 'support cache types: $AVAILABLE_MODES'
        exit 1
fi 

# Broker management

AVAILABLE_BROKER_TYPES='redis none'
APP_BROKER_TYPE_VALID=`echo $AVAILABLE_BROKER_TYPES | grep $APP_BROKER_TYPE | wc -l`
if [ "$APP_BROKER_TYPE_VALID" -eq 0 ]; then
        echo >&2 'Specified broker type is invalid: $APP_BROKER_TYPE;'
        echo >&2 'support broker types: $AVAILABLE_BROKER_TYPES'
        exit 1
fi

if [ "$APP_BROKER_TYPE" != 'none' ] && { [ -z "$APP_BROKER_HOST" ] || [ -z "$APP_BROKER_PORT" ]; }; then
        echo >&2 'You have specified a broker type, please set following environment variables'
        echo >&2 'APP_BROKER_HOST and APP_BROKER_PORT.'
        exit 1
fi

# DB management

if [ "$APP_USE_LOCAL_DB" != 'true' ] && { [ -z "$APP_DB_DRIVER" ] || [ -z "$APP_DB_HOST" ] || [ -z "$APP_DB_PORT" ] || [ -z "$APP_DB_USER" ] || [ -z "$APP_DB_PASSWORD" ]; }; then
	echo >&2 'Error, you did not specify the usage of a local db (set env APP_USE_LOCAL_DB to true;'
	echo >&2 'Please fill following variables $APP_DB_DRIVER, $APP_DB_HOST, $APP_DB_PORT, $APP_DB_USER and $APP_DB_PASSWORD;'
        exit 1
fi

if [ "$APP_USE_LOCAL_DB" == 'true' ]; then
	APP_DATABASE_URI="sqlite:////home/superset/.superset/superset.db"
else
	APP_DATABASE_URI="$APP_DB_DRIVER://$APP_DB_USER:$APP_DB_PASSWORD@$APP_DB_HOST:$APP_DB_PORT/superset"
fi

# Cache config management


if [ "$APP_CACHE_TYPE" == 'redis' ]; then
	cat /opt/superset_templates/redis_cache_config.tpl >> /opt/superset/superset_config.py
fi

# Broker config management

if [ "$APP_BROKER_TYPE" == 'redis' ]; then
        cat /opt/superset_templates/redis_broker_config.tpl >> /opt/superset/superset_config.py
fi

# Admin creation

if [ -z "$APP_ADMIN_USER_PASSWORD" ]; then
	echo >&2 'Error: A password must be provided for admin user '
	echo >&2 'Specify either a APP_ADMIN_USER_PASSWORD env parameter of a APP_ADMIN_USER_PASSWORD_FILE pointing to an existing file in the container '
	exit 1
fi

# Config setup

#APP_SECRET_KEY=`openssl rand -base64 25`
APP_SECRET_KEY='LCcgJCzHbp1LM1TTg+m0n8sb2iPYhk4flg=='

sed -i 's~$APP_SECRET_KEY~'"$APP_SECRET_KEY"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_DATABASE_URI~'"$APP_DATABASE_URI"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_CACHE_HOST~'"$APP_CACHE_HOST"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_CACHE_PORT~'"$APP_CACHE_PORT"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_CACHE_AUTH~'"$APP_CACHE_AUTH"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_BROKER_HOST~'"$APP_BROKER_HOST"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_BROKER_PORT~'"$APP_BROKER_PORT"'~g' "/opt/superset/superset_config.py"
sed -i 's~$APP_TIMEOUT~'"$APP_TIMEOUT"'~g' "/opt/superset/superset_config.py"



if [ "$APP_CACHE_TYPE" != 'none' ]; then
	APP_CACHE_URI="$APP_CACHE_TYPE://$APP_CACHE_AUTH$APP_CACHE_HOST:$APP_CACHE_PORT"
else
	APP_CACHE_URI="none"
fi

if [ "$APP_BROKER_TYPE" != 'none' ]; then
        APP_BROKER_URI="$APP_BROKER_TYPE://$APP_BROKER_HOST:$APP_BROKER_PORT/0"
else
        APP_BROKER_URI="none"
fi

# Probes

sed -i 's~$DB_URI~'"$APP_DATABASE_URI"'~g' "/opt/superset_probes/probes.cfg"
sed -i 's~$CACHE_URI~'"$APP_CACHE_URI"'~g' "/opt/superset_probes/probes.cfg"
sed -i 's~$BROKER_URI~'"$APP_BROKER_URI"'~g' "/opt/superset_probes/probes.cfg"

if [ "$APP_USE_LOCAL_DB" != 'true' ]; then
	python /opt/superset_probes/db_wait.py
fi

echo '**** Running with configuration ****'
cat /opt/superset/superset_config.py

ADMIN_EXISTS=`fabmanager list-users --app superset| grep username:admin | wc -l`

if [ "$ADMIN_EXISTS" -eq 0 ]; then
        echo 'Creating admin user for superset'
	fabmanager create-admin --app superset \
		--username $APP_ADMIN_USER --firstname $APP_ADMIN_USER_FN --lastname $APP_ADMIN_USER_LN --email $APP_ADMIN_USER_EMAIL \
		--password $APP_ADMIN_USER_PASSWORD
fi

superset db upgrade
superset init

if [ "$APP_SUPERSET_MODE" == 'default' ]; then
        echo '****** SUPERSET : Running as server ******'
	superset runserver
elif [ "$APP_SUPERSET_MODE" == 'worker' ]; then
        echo '****** SUPERSET : Running as worker ******'
	superset worker
fi

exit 0
