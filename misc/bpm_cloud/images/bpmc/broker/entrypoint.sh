#!/bin/bash

# file_env func has been taken from the rabbitmq original entrypoint
# see https://github.com/docker-library/rabbitmq/blob/master/3.7/alpine/docker-entrypoint.sh

file_env() {
	local var="$1"
	local fileVar="${var}_FILE"
	local def="${2:-}"
	if [ "${!var:-}" ] && [ "${!fileVar:-}" ]; then
		echo >&2 "error: both $var and $fileVar are set (but are exclusive)"
		exit 1
	fi
	local val="$def"
	if [ "${!var:-}" ]; then
		val="${!var}"
	elif [ "${!fileVar:-}" ]; then
		val="$(< "${!fileVar}")"
	fi
	export "$var"="$val"
	unset "$fileVar"
}

fileEnvKeys=(erlang_cookie)
for fileEnvKey in "${fileEnvKeys[@]}"; do file_env "RABBITMQ_${fileEnvKey^^}"; done

exec /usr/local/bin/docker-entrypoint.sh "$@"