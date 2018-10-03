call %LOCALAPPDATA%\conda\conda\envs\IBIS\Scripts\activate.bat
call activate IBIS

set "logpath=%USERPROFILE%\Desktop\celery.log"

start python -m flower -A data_quality --broker=amqp://dq:ibis_system@localhost/data_quality -f %logpath%
timeout /t 2
start python -m celery -A data_quality worker -l info -Q Periodic -n periodic_worker -c 1 -f %logpath%
start python -m celery -A data_quality worker -l info -Q Logic -n logic_worker -c 4 -f %logpath%
start python -m celery -A data_quality worker -l info -Q Persistence -n persistence_worker -c 2 -f %logpath%
start python -m celery -A data_quality worker -l info -Q ETL -n etl_worker -c 1 -f %logpath%
timeout /t 10
start python -m celery -A data_quality beat

pause
call deactivate