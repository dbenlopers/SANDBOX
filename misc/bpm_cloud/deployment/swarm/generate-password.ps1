New-Item -ItemType Directory -Force -Path passwords
Set-Item -path env:RANDFILE -value ".rnd"
openssl rand -base64 10 -out passwords/APP_DATABASE_PASSWORD
openssl rand -base64 10 -out passwords/APP_DATABASE_ROOT_PASSWORD
openssl rand -base64 10 -out passwords/APP_BROKER_PASSWORD
openssl rand -base64 10 -out passwords/APP_ROLETOKEN
openssl rand -base64 10 -out passwords/APP_CPTTOKEN
openssl rand -base64 10 -out passwords/APP_WEBDAV_PASSWORD
openssl rand -base64 10 -out passwords/APP_BROKER_COOKIE
openssl rand -base64 10 -out passwords/APP_STORAGE_DAV_PASSWORD