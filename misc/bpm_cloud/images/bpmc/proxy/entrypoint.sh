#!/bin/sh

APP_PUBLIC_API_HOST=${APP_PUBLIC_API_HOST:-api.public}
APP_PUBLIC_API_PORT=${APP_PUBLIC_API_PORT:-80}
APP_AVAILABLE_API_HOST=${APP_AVAILABLE_API_HOST:-api.available}
APP_AVAILABLE_API_PORT=${APP_AVAILABLE_API_PORT:-80}

sed -i 's~$APP_PUBLIC_API_HOST~'"$APP_PUBLIC_API_HOST"'~g'    /etc/nginx/conf.d/default.conf
sed -i 's~$APP_PUBLIC_API_PORT~'"$APP_PUBLIC_API_PORT"'~g'    /etc/nginx/conf.d/default.conf
sed -i 's~$APP_AVAILABLE_API_HOST~'"$APP_AVAILABLE_API_HOST"'~g'    /etc/nginx/conf.d/default.conf
sed -i 's~$APP_AVAILABLE_API_PORT~'"$APP_AVAILABLE_API_PORT"'~g'    /etc/nginx/conf.d/default.conf

until ping -c1 $APP_PUBLIC_API_HOST  &>/dev/null; do echo >&2 'Waiting for Public api to be up' && sleep 5; done
until ping -c1 $APP_AVAILABLE_API_HOST  &>/dev/null; do echo >&2 'Waiting for Available api to be up' && sleep 5; done

echo '**************************************************'
echo "Starting BPMc proxy with config"
echo "Public service redirects on: http://$APP_PUBLIC_API_HOST:$APP_PUBLIC_API_PORT"
echo "Available service redirects on: http://$APP_AVAILABLE_API_HOST:$APP_AVAILABLE_API_PORT"
echo '**************************************************'

nginx -g 'daemon off;'

exit 0