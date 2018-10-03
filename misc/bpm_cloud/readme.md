# BPM Cloud application

## Contents

This repository contains the ```ge.bpmc``` python module and the necessary files to build the associated docker image.
It also contains files to build required images to use the BPM Cloud application in a Docker environment.
See [images/readme.md](./images/readme.md) for more details.
Finally, you can found how to deploy this application in a staging/production environment using this application's [deployment/readme.md](./deployment/readme.md).

## Requirements

This application requires two external components:
- A broker (we recommend using RabbitMQ)
- A database (either MySQL 5.7+ or MariaDB 10.2+, we are using JSON types which might not be supported by other DBMSes)

## Installation / Development

### Dependencies management and registration

This modules has dependencies that can be installed through multiples ways.

On a **production** environment, just run a python module installation command in the [ge.bpmc](./ge.bpmc) folder.
```sh
python setup.py install
```
or
```sh
pip install .
```

On a **development** environment, switch to the following command:
```sh
python setup.py develop
```
or
```sh
pip install -e .
```

> ___What's the difference ?___

The _install_ command will compile and copy the files in the python repository. This means that if the code is changed in the module, it won't be in the python repository.

The _develop_ command will link the module in the python repository, meaning that you can see your changes directly by restarting the application.

Both will read the [setup.py](./ge.bpmc/setup.py) file and install dependencies.

### Celery & Windows

Since 4.x versions, Celery does not **officially** supports Windows, although it works well with a simple tweak: use **eventlet** as pool library.
Since this library work on both **Windows** and **Linux**, workers are launched with **eventlet** as the **default pooling library**. See [WorkerApplication](./ge.bpmc/ge/bpmc/app/default.py).

### Tests dependencies

To run tests, you will need to install dependencies listed in the ```extras_require``` section's _test_ profile.

Go in the [ge.bpmc](./ge.bpmc) folder and run:
```sh
pip install -e .[test]
```

Please be **advised** that this will act as the ```python develop``` / ```python install -e``` command and will link the module in your local repository.

## Database configuration

Please use the following configuration for your database collations:
```sql
[mysql]
default-character-set=utf8

[mysqld]
collation-server = utf8_bin
init-connect='SET NAMES utf8'
character-set-server = utf8
```

## Running the tests

First, setup your connection string to the database using environment variable **BPM_UT_DB**:

```ps1
Set-Item -path env:BPM_UT_DB -value "mysql+pymysql://root:root@127.0.0.1:3306/test"
```
or
```sh
export BPM_UT_DB="mysql+pymysql://root:root@127.0.0.1:3306/test"
```

Simply run the following command:

```python
python -m unittest discover -s ge.bpmc -p 'test_*.py'
```

Please be **advised** that tests require a MySQL/MariaDB database to run and that a "test" scheme needs to be created. Please use the 'utf8_bin' collation to create the database.

## Running the application

Use the [ge.bpmc.app.runner](./ge.bpmc/ge/bpmc/app/runner.py) to run the expected components. Check the file to view available options.
This will require a configuration file for the application and for the logging. Please see [config.cfg.example](./ge.bpmc/docs/app/config.cfg.example) and [logging.yml](./ge.bpmc/docs/app/logging.yml). A detailed section covers configuration options.

Once your configuration is ready use the following command:

```sh
python -m ge.bpmc.app.runner $app_type $app_module $path_to_config_file
```
For example:
```sh
python -m ge.bpmc.app.runner api storage api_storage.cfg
python -m ge.bpmc.app.runner api public api_public.cfg
python -m ge.bpmc.app.runner worker processing broker.cfg
```

As you might have seen in the runner, this application contains 7 components:
- Public API (```api public```)
- Storage API (```api storage```)
- Available API (```api available```)
- Processing Worker (```worker processing```)
- Periodic Worker (```worker periodic```)
- Matching Worker (```worker matching```)
- Periodic Beater (```beater periodic```)

## Docker images & deployment

Please see the appropriate files:
- [images readme.md](./images/readme.md)
- [deployment readme.md](./deployment/readme.md)

## Configuration management

Some keys are mandatory but required keys vary based on the type of application run and its options.

Mandatory (required configuration for the component to work): ![Mandatory](./ge.bpmc/docs/images/mandatory.png)
Affects (component affected by this parameter): ![Affects](./ge.bpmc/docs/images/affects.png)

|  | Database | Broker | Webdav | Storage API | Application/ignite | Application/profiling | Application/roletoken | Application/cpnttoken |  Logging |
| ---------- | -------- | ------ | ----------- | ------ | ------------------ | --------------------- | --------------------- | --------------------- | ------- |
| Public API | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Affects](./ge.bpmc/docs/images/affects.png) | ![Affects](./ge.bpmc/docs/images/affects.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |
| Storage API | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |  ![Mandatory](./ge.bpmc/docs/images/mandatory.png) (if access to webdav requires a specific configuration) | | ![Affects](./ge.bpmc/docs/images/affects.png) | ![Affects](./ge.bpmc/docs/images/affects.png) | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |
| Available API | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Affects](./ge.bpmc/docs/images/affects.png) | ![Affects](./ge.bpmc/docs/images/affects.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |
| Processing Worker | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | ![Affects](./ge.bpmc/docs/images/affects.png) | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |
| Periodic Worker | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | | | ![Affects](./ge.bpmc/docs/images/affects.png) | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |
| Matching Worker | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | | | ![Affects](./ge.bpmc/docs/images/affects.png) | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) |
| Periodic Beater | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png) | | | |  | | | ![Mandatory](./ge.bpmc/docs/images/mandatory.png)

For example, webdav configuration is only mandatory for the ```storage api```.

Here is a detailed analysis of the application **configuration file**:

### Database

```
[database]
dsn=mysql+pymysql://root:root@127.0.0.1:3306/bpm
```

The database section, for obvious reasons, contains the dsn chain used to access the database.

Here is the syntax:
```$driver(+$dialect)://$user:$password@$host:$port/$schema```

Since this application is designed to run on a mysqlish database, the driver should not change. By default this application installs the ```pymysql``` module and we **strongly** recommand using it.

### Broker

```
[broker]
dsn=amqp://guest:guest@127.0.0.1:5672
```

Same, broker section for obvious reasons contains the dsn chain to access the broker.

Syntax used is:
```$protocol://$user:$password@$host:$port```

Used protocol depends on the broker. RabbitMQ is the expected broker for this application and we advise to connect using ```amqp```.

### Webdav

Those sections are optional. ```webdav_opts``` and ```webdav_client_opts``` are used to pass parameters when connecting to repositories.
```webdav_opts``` contains information used by the connection itself and ```webdav_client_opts``` is used to declare options passed to the ```requests``` module.

```
[webdav_opts]
# In case of proxy...
# proxy_hostname=
# proxy_login=
# proxy_password=

# If you want to login using certificate
# ssl_auth_cert_path=
# ssl_auth_key_path=

# Basic authentication
auth_login=dave
auth_password=dave

[webdav_client_opts]
# Allows to that the certificate authority to accept self signed certificates
verify=C:\Users\502676073\Documents\4-IB\BPM\dovelCA.crt
```

_In-depth explanation_
```
proxy_hostname=
proxy_login=
proxy_password=
```
Those parameters are used if a proxy is to be used when connecting to the repository. Nothing fancy here. ```proxy_hostname``` acts as classic proxy declaration (you can specify the protocol used and port if necessary).

```
ssl_auth_cert_path=
ssl_auth_key_path=
```
Those are used when you want to authenticate on the webdav server using an ssl certificate and its associated key.

```
auth_login=
auth_password=
```
Those are used for a basic authentication on the webdav server using a classic .htpasswd file.

```
verify=
```
So this is more fancy. As previously stated, this is used when you want to pass parameters to python's **requests** module. ```verify``` is used to provide a Certification Authority certificate. This is to be used when you want to access to your webdav server using **SSL** with a **self-signed certificate**.
Please check the [official documentation](http://docs.python-requests.org/en/master/user/advanced/#ssl-cert-verification).

### Storage API

```
[storage]
uri=localhost:9080
proto=http
```
This is used when a connectivity to the ```storage api``` is required. Simply specify the protocol and base url to use to access to the api.

### Application

This section is used by every components although mandatory parameters and or affected components may vary.

```
[application]
ignite=false
profiling=false
roletoken=XXXXX
cpnttoken=XXXXX
```

```ignite``` **affects** only APIs. If true, the application will try to deploy the schema on the database. If the table already exists, does nothing (this means you can restart your application with the ignite option set to *true* without having any issue).

```profiling``` **affects** all APIs and Workers. If set to true, the application will profile a set of feature.
You can found affected features [here](./ge.bpmc/ge/bpmc/utilities/profiling.py). See **setup_task_profiling** and **setup_resource_profiling** methods.

```roletoken``` and ```cpnttoken``` are used to setup access tokens. The ```roletoken``` is used for external access while ```cpnttoken``` is used to authentication application components.
```roletoken``` is **mandatory** for:
- Public API
- Storage API

```cpnttoken``` is **mandatory** for:
- Public API
- Storage API
- Available API
- Processing Worker
- Matching Worker

### Logging

**Mandatory** for **all** components.

```
[logging]
configuration=/path/to/logging.yml
```

This sets the path to the logging.yml configuration. Check the [logging.yml](./ge.bpmc/docs/app/logging.yml) example.