#!/bin/sh

if [ -z ${APP_CPTTOKEN+x} ] && { [ ! -z ${APP_CPTTOKEN_FILE+x} ] && [ -f $APP_CPTTOKEN_FILE ]; }; then
    APP_CPTTOKEN=$(cat $APP_CPTTOKEN_FILE)
fi

if [ -z ${CPT_WEBDAV_PASSWD+x} ] && { [ ! -z ${CPT_WEBDAV_PASSWD_FILE+x} ] && [ -f $CPT_WEBDAV_PASSWD_FILE ]; }; then
    CPT_WEBDAV_PASSWD=$(cat $CPT_WEBDAV_PASSWD_FILE)
fi

if [ -z $CPT_WEBDAV_USER ] || [ -z $CPT_WEBDAV_PASSWD ]; then
    echo >&2 'error: missing credentials for webdav account:'
    echo >&2 "- CPT_WEBDAV_USER, got '$CPT_WEBDAV_USER'"
    echo >&2 "- CPT_WEBDAV_PASSWD, got '$CPT_WEBDAV_PASSWD'"
    exit 1
fi

APP_PUBLIC_API_PORT=${APP_PUBLIC_API_PORT:-8080}

if [ -z $CPT_REPO_NAME ] || [ -z $APP_PUBLIC_API_HOST ] || [ -z $APP_CPTTOKEN ]; then
    echo >&2 'error: missing registration parameters:'
    echo >&2 "- CPT_REPO_NAME, got '$CPT_REPO_NAME'"
    echo >&2 "- APP_PUBLIC_API_HOST, got '$APP_PUBLIC_API_HOST'"
    echo >&2 "- APP_PUBLIC_API_PORT, got '$APP_PUBLIC_API_PORT'"
    echo >&2 "- APP_CPTTOKEN, got '$APP_CPTTOKEN'"
    exit 1
fi

CPT_REPO_HOST=${CPT_REPO_HOST:-$CPT_REPO_NAME}

# Update payload for automated repository registry

sed -i 's~$CPT_REPO_NAME~'"$CPT_REPO_NAME"'~g'    /service-registry.json
sed -i 's~$CPT_REPO_HOST~'"$CPT_REPO_HOST"'~g'    /service-registry.json

# Password generation

printf "$CPT_WEBDAV_USER:$(openssl passwd -apr1 $CPT_WEBDAV_PASSWD)\n" > /var/www/webdav/.htpasswd

# Repository registration

until ping -c1 $APP_PUBLIC_API_HOST  &>/dev/null; do echo >&2 'Waiting for Public service to be up' && sleep 5; done
until curl -X POST -H "Content-Type: application/json" -H "X-BPM-Component-Key: $APP_CPTTOKEN" --silent --data-binary "@/service-registry.json" -o /dev/null http:/$APP_PUBLIC_API_HOST:$APP_PUBLIC_API_PORT/repository; do echo >&2 'Waiting for registration' && sleep 5; done

echo '**************************************************'
echo "Starting BPMc Webdav repository '$CPT_REPO_NAME'"
echo '**************************************************'

nginx -g 'daemon off;'

exit 0