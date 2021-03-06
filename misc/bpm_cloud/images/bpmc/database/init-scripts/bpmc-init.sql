CREATE DATABASE IF NOT EXISTS bpm COLLATE 'utf8_bin';
GRANT ALL ON bpm.* TO 'bpm'@'localhost' IDENTIFIED BY '$APP_DATABASE_PASSWORD' WITH GRANT OPTION;
GRANT ALL ON bpm.* TO 'bpm'@'%' IDENTIFIED BY '$APP_DATABASE_PASSWORD' WITH GRANT OPTION;
FLUSH PRIVILEGES;