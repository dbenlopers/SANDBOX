#!/bin/sh

mkdir -p passwords
openssl rand -base64 10 > passwords/APP_DB_ROOT_PASSWORD
openssl rand -base64 10 > passwords/APP_DB_SUPERSET_PASSWORD
openssl rand -base64 10 > passwords/APP_ADMIN_USER_PASSWORD
