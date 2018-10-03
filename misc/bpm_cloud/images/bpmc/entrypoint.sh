#!/bin/sh

if [ -z $CPT_TYPE ] || [ -z $CPT_APP ]; then
    echo >&2 'error: missing main initialization argument, please specify:'
    echo >&2 "- CPT_TYPE, got '$CPT_TYPE'"
    echo >&2 "- CPT_APP, got '$CPT_APP'"
    exit 1
fi

DEFAULT_OPT_VALUE=false
APP_DATABASE_PROTO=${APP_DATABASE_PROTO:-mysql+pymysql}
APP_BROKER_PROTO=${APP_BROKER_PROTO:-amqp}
APP_DATABASE_USER=${APP_DATABASE_USER:-bpm}
APP_BROKER_USER=${APP_BROKER_USER:-guest}

APP_STORAGE_HOST=${APP_STORAGE_HOST:-bpmstorageapi}
APP_STORAGE_PORT=${APP_STORAGE_PORT:-8080}
APP_STORAGE_PROTO=${APP_STORAGE_PROTO:-http}

APP_STORAGE_DAV_USE_SSL=${APP_STORAGE_DAV_USE_SSL:-$DEFAULT_OPT_VALUE}
APP_STORAGE_DAV_LOGIN=${APP_STORAGE_DAV_LOGIN:-dave}
APP_STORAGE_DAV_PASSWORD=${APP_STORAGE_DAV_PASSWORD:-dave}

CPT_IGNITE=${CPT_IGNITE:-$DEFAULT_OPT_VALUE}
CPT_PROFILING=${CPT_PROFILING:-$DEFAULT_OPT_VALUE}
CPT_LOGLEVEL=${CPT_LOGLEVEL:-INFO}
CPT_REQUIRE_DB=${CPT_REQUIRE_DB:-DEFAULT_OPT_VALUE}

if [ -z ${APP_DATABASE_PASSWORD+x} ] && { [ ! -z ${APP_DATABASE_PASSWORD_FILE+x} ] && [ -f $APP_DATABASE_PASSWORD_FILE ]; }; then
    APP_DATABASE_PASSWORD=$(cat $APP_DATABASE_PASSWORD_FILE)
fi

if [ -z ${APP_BROKER_PASSWORD+x} ] && { [ ! -z ${APP_BROKER_PASSWORD_FILE+x} ] && [ -f $APP_BROKER_PASSWORD_FILE ]; }; then
    APP_BROKER_PASSWORD=$(cat $APP_BROKER_PASSWORD_FILE)
fi

if [ -z ${APP_ROLETOKEN+x} ] && { [ ! -z ${APP_ROLETOKEN_FILE+x} ] && [ -f $APP_ROLETOKEN_FILE ]; }; then
	APP_ROLETOKEN=$(cat $APP_ROLETOKEN_FILE)
fi

if [ -z ${APP_CPTTOKEN+x} ] && { [ ! -z ${APP_CPTTOKEN_FILE+x} ] && [ -f $APP_CPTTOKEN_FILE ]; }; then
	APP_CPTTOKEN=$(cat $APP_CPTTOKEN_FILE)
fi

APP_ROLETOKEN=${APP_ROLETOKEN:-0000XXXX00000XX}
APP_CPTTOKEN=${APP_CPTTOKEN:-0000XXXX00000XX}

if { [ ! -z ${APP_STORAGE_DAV_PASSWORD_FILE+x} ] && [ -f $APP_STORAGE_DAV_PASSWORD_FILE ]; }; then
	APP_STORAGE_DAV_PASSWORD=$(cat $APP_STORAGE_DAV_PASSWORD_FILE)
fi

if [ -z $APP_DATABASE_PASSWORD ]; then
    echo >&2 'error: missing database connectivity argument, please specify:'
    echo >&2 "- APP_DATABASE_PASSWORD or APP_DATABASE_PASSWORD_FILE"
    exit 1
fi

if [ -z $APP_BROKER_PASSWORD ]; then
    echo >&2 'error: missing database connectivity argument, please specify:'
    echo >&2 "- APP_BROKER_PASSWORD or APP_BROKER_PASSWORD_FILE"
    exit 1
fi

APP_DATABASE_DSN=${APP_DATABASE_DSN:-bpmdb:3306/bpm}
APP_BROKER_DSN=${APP_BROKER_DSN:-bpmbk:5672}
APP_DATABASE_DSN_FULL="$APP_DATABASE_PROTO://$APP_DATABASE_USER:$APP_DATABASE_PASSWORD@$APP_DATABASE_DSN"
APP_BROKER_DSN_FULL="$APP_BROKER_PROTO://$APP_BROKER_USER:$APP_BROKER_PASSWORD@$APP_BROKER_DSN"

sed -i 's~$CPT_LOGLEVEL~'"$CPT_LOGLEVEL"'~g' $CPT_LOG_CONFIG_FILE

sed -i 's~$APP_DATABASE_DSN~'"$APP_DATABASE_DSN_FULL"'~g' $CPT_CFG_FILE
sed -i 's~$APP_BROKER_DSN~'"$APP_BROKER_DSN_FULL"'~g' $CPT_CFG_FILE
sed -i 's~$APP_STORAGE_DAV_USE_SSL~'"$APP_STORAGE_DAV_USE_SSL"'~g' $CPT_CFG_FILE
sed -i 's~$APP_STORAGE_DAV_LOGIN~'"$APP_STORAGE_DAV_LOGIN"'~g' $CPT_CFG_FILE
sed -i 's~$APP_STORAGE_DAV_PASSWORD~'"$APP_STORAGE_DAV_PASSWORD"'~g' $CPT_CFG_FILE
sed -i 's~$APP_STORAGE_HOST~'"$APP_STORAGE_HOST"'~g' $CPT_CFG_FILE
sed -i 's~$APP_STORAGE_PORT~'"$APP_STORAGE_PORT"'~g' $CPT_CFG_FILE
sed -i 's~$APP_STORAGE_PROTO~'"$APP_STORAGE_PROTO"'~g' $CPT_CFG_FILE
sed -i 's~$APP_ROLETOKEN~'"$APP_ROLETOKEN"'~g' $CPT_CFG_FILE
sed -i 's~$APP_CPTTOKEN~'"$APP_CPTTOKEN"'~g' $CPT_CFG_FILE
sed -i 's~$CPT_PROFILING~'"$CPT_PROFILING"'~g' $CPT_CFG_FILE
sed -i 's~$CPT_IGNITE~'"$CPT_IGNITE"'~g' $CPT_CFG_FILE
sed -i 's~$CPT_LOG_CONFIG_FILE~'"$CPT_LOG_CONFIG_FILE"'~g' $CPT_CFG_FILE

if [ $CPT_REQUIRE_DB = "true" ] || [ $CPT_IGNITE = "true" ]; then
    echo 'Checking database availability'
    python /usr/local/bin/db_probe.py
fi

echo '**************************************************'
echo "Starting component $CPT_TYPE/$CPT_APP with params:"
echo "Database: $APP_DATABASE_DSN_FULL"
echo "Broker: $APP_BROKER_DSN_FULL"
echo "Role Token: $APP_ROLETOKEN"
echo "Component Token: $APP_CPTTOKEN"
echo 'Opts'
echo '----'
echo "Require db: $CPT_REQUIRE_DB"
echo "Ignite: $CPT_IGNITE"
echo "Profiling: $CPT_PROFILING"
echo "Loglevel: $CPT_LOGLEVEL"
echo '**************************************************'

python -m ge.bpmc.app.runner $CPT_TYPE $CPT_APP $CPT_CFG_FILE

exit 0