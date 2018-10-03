# IBIS Schema

## Contents

This file details how to deploy the IBIS schema and what is deployed.

## Requirements

- MySQL-ish database (IBIS is bound to MySQL due to its usage of JSON data type)
- 3 schemas: one for the application database, one for its datamarts and one for its archives

## Deployment

A **full** deployment method is available in the module's [\_\_init\_\_.py file](../ge/ibis/entities/__init__.py) named ```deploy_stack```.

Its arguments are:
- main_session: the session to use to connect to the application's schema
- data_session: the session to use to connect to the application's datamarts schema
- archive_session: the session to use to connect to the application's archive schema
- (optional) data_schema_name: default is "**data**".

Simply run this method as in the example bellow:
```python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ge.ibis.entities import deploy_stack

main_dsn = 'mysql+pymysql://root:root@127.0.0.1:3306/ibis'
data_dsn = 'mysql+pymysql://root:root@127.0.0.1:3306/ibis_data'
archive_dsn = 'mysql+pymysql://root:root@127.0.0.1:3306/ibis_archive'
main_eng = create_engine(main_dsn)
data_eng = create_engine(data_dsn)
archive_eng = create_engine(archive_dsn)
main_session_factory = sessionmaker(bind=main_eng)
data_session_factory = sessionmaker(bind=data_eng)
archive_session_factory = sessionmaker(bind=archive_eng)
main_session = main_session_factory()
data_session = data_session_factory()
archive_session = archive_session_factory()

deploy_stack(main_session, data_session, archive_session, 'ibis_data')

main_session.close()
data_session.close()
archive_session.close()
```


