# BPMc side images folder

## Contents

This folder contains the images of:
* BPMc database
* BPMc repository
* BPMc proxy
* BPMc broker

The main image is building using the root directory's [Dockerfile](../Dockerfile)

This folder also contains configuration files of the BPMc application: [application entrypoint](./bpmc/entrypoint.sh), [application config](./bpmc/config.cfg) and [application logging config](./bpmc/logging.yml).
See the [application dockerfile](../Dockerfile) for more details.

## Naming

Expected image names are the following
* Main: bpmc_app
* Proxy: bpmc_proxy
* Repository: bpmc_repo
* Broker: bpmc_broker
* Database: bpmc_db

## Build arguments

If you're building inside GE's network, you'll need to specify the proxy when building image:
```bash
--build-arg HTTP_PROXY=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80 --build-arg HTTPS_PROXY=http://PITC-Zscaler-EMEA-Amsterdam3PR.proxy.corporate.ge.com:80
```

## How to build

Do not forget you need to be in the folder __containing__ the Dockerfile when building because it uses the current folder as the building context.

## Supported container arguments

This section details supported container arguments.

| Scope | Description |
| ----- | ----------- |
| APP_ | Variables used in multiple components of the application |
| CPT_ | Variables used only in this component |

### BPMC APP

Some items are mandatory only for specific components.
Check the configuration matrix in [main readme](../readme.md).

| Name | Default value | Description |
| ---- | ------------- | ----------- |
| CPT_TYPE | None | ```app_type``` argument of the ```ge.bpmc.app.runner```
| CPT_APP | None | ```app_module``` argument of the ```ge.bpmc.app.runner```
| CPT_IGNITE | False | Ignite option of the application configuration | 
| CPT_PROFILING | False | Profiling option of the application configuration |
| CPT_LOGLEVEL | WARN | Root log level of the application |
| CPT_REQUIRE_DB | False | Determines if the container has to wait for the database to be available before start. Overrode by ```CPT_IGNITE``` if ignite is set to True. |
| APP_DATABASE_PROTO | mysql+pymysql | Driver & dialect to use to connect to the database. Some drivers or dialects require python package to be installed. |
| APP_DATABASE_USER | bpm | User used to connect to the database |
| APP_DATABASE_PASSWORD | None | Password used to connect to the database. **Mandatory**. |
| APP_DATABASE_PASSWORD_FILE | None | Provide a file path used to read the database's password. This is useful when using secrets to provide passwords to the application. Has an effect only if ```APP_DATABASE_PASSWORD``` is not set. |
| APP_BROKER_PROTO | amqp | Default protocol used to connect to the message broker |
| APP_BROKER_USER | guest | User used to connect to the broker |
| APP_BROKER_PASSWORD | None | Password used to connect to the broker. **Mandatory**. |
| APP_BROKER_PASSWORD_FILE | None | Provide a file path used to read the broker's password. This is useful when using secrets to provide passwords to the application. Has an effect only if ```APP_BROKER_PASSWORD``` is not set. |
| APP_STORAGE_HOST | bpmstorageapi | Host of the Storage API |
| APP_STORAGE_PORT | 8080 | Storage API listening port |
| APP_STORAGE_PROTO | http | Protocol to use to connect to the Storage API |
| APP_STORAGE_DAV_LOGIN | dave | User to log on the Webdav repository. **mandatory** in the Dockerized application. |
| APP_STORAGE_DAV_PASSWORD | dave | Password to log on the Webdav repository. **mandatory** in the Dockerized application. |
| APP_STORAGE_DAV_PASSWORD_FILE | None | Provide a file path used to read the webdav's password. This is useful when using secrets to provide passwords to the application. **Overrides** ```APP_STORAGE_DAV_PASSWORD```. |
| APP_ROLETOKEN | 0000XXXX00000XX | Role token to use in the application |
| APP_ROLETOKEN_FILE | None | When you want the role token to be read from a filepath. Only effective if APP_ROLETOKEN is not set. |
| APP_CPTTOKEN | 0000XXXX00000XX
| APP_CPTTOKEN_FILE | None | When you want the component token to be read from a filepath. Only effective if APP_CPTTOKEN is not set. |

### BPMC Proxy

| Name | Default value | Description |
| ---- | ------------- | ----------- |
| APP_PUBLIC_API_HOST | api.public | Host of the Public API | 
| APP_PUBLIC_API_PORT | 80 | Port of the Public API | 
| APP_AVAILABLE_API_HOST | api.available | Host of the Available API | 
| APP_AVAILABLE_API_PORT | 80 | Port of the Available API | 

### BPMC Repository

| Name | Default value | Description |
| ---- | ------------- | ----------- |
| APP_PUBLIC_API_HOST | None | Host of the Public API. **mandatory**. | 
| APP_PUBLIC_API_PORT | 8080 | Port of the Public API | 
| APP_CPTTOKEN | None | Component token. **mandatory**. |
| APP_CPTTOKEN_FILE | None | Used to read the component token from a file if ```APP_CPTTOKEN``` is empty.
| CPT_WEBDAV_USER | None | The webdav repository user. **mandatory**. |
| CPT_WEBDAV_PASSWD | None | The webdav repository password. **mandatory**. |
| CPT_WEBDAV_PASSWD_FILE | None | Used to read the webdav password from a file if ```CPT_WEBDAV_PASSWD``` is empty. |
| CPT_REPO_NAME | None | The repository name. **mandatory**. |

### BPMC Database

| Name | Default value | Description |
| ---- | ------------- | ----------- |
| MYSQL_ROOT_PASSWORD | None | Root password of the database. **mandatory**. |
| MYSQL_ROOT_PASSWORD_FILE | None | Used to read the password from a file if ```MYSQL_ROOT_PASSWORD``` is empty. |
| APP_DATABASE_PASSWORD | None | ```bpm``` user password of the database. **mandatory**. |
| APP_DATABASE_PASSWORD_FILE | None | Used to read the password from a file if ```APP_DATABASE_PASSWORD``` is empty. |
| CPT_INNODB_BUFFER_POOL_SIZE | 2G | InnoDB buffer pool size. |

### BPMC Broker

See [RabbitMQ Alpine original image](https://github.com/docker-library/rabbitmq/blob/master/3.7/alpine/docker-entrypoint.sh) for more details.

| Name | Default value | Description |
| ---- | ------------- | ----------- |
| RABBITMQ_ERLANG_COOKIE_FILE | None | Used to read the cookie hash from a file if ```RABBITMQ_ERLANG_COOKIE``` is empty. |


