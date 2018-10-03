#!/bin/sh
mkdir -p passwords
openssl rand -base64 10 > passwords/APP_DATABASE_PASSWORD
openssl rand -base64 10 > passwords/APP_DATABASE_ROOT_PASSWORD
openssl rand -base64 10 > passwords/APP_BROKER_PASSWORD
openssl rand -base64 10 > passwords/APP_ROLETOKEN
openssl rand -base64 10 > passwords/APP_CPTTOKEN
openssl rand -base64 10 > passwords/APP_WEBDAV_PASSWORD
openssl rand -base64 10 > passwords/APP_BROKER_COOKIE
openssl rand -base64 10 > passwords/APP_STORAGE_DAV_PASSWORD