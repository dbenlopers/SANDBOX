#!/bin/bash

# Worker concurrency parameters
declare -A Worker=(["Periodic"]=1 ["Logic"]=1 ["Persistence"]=1 ["ETL"]=3)

# Python env parameters
PYTHON_ENV_NAME=ibisvenv

APP=data_quality

# logging parameters
LOG_PATH=/var/log/celery/celeryd.log
LOG_LEVEL=info

LOG_PATH_BEAT=/var/log/celery/celerybeatd.log
LOG_LEVEL_BEAT=info


# Function that start celery monitoring, worker and beat
start() {

    echo "Activate Python venv"
    source activate $PYTHON_ENV_NAME
    
    echo "Start Celery monitoring"
    flower -A $APP --broker=amqp://dq:ibis_system@localhost/data_quality &
    
    sleep 2
    
    for i in "${!Worker[@]}"
    do
        echo "Start worker: "$i
        # celery -A $APP worker -Q $i -n $i"@%h" -l $LOG_LEVEL -c ${Worker[$i]} &
        celery -A $APP worker -Q $i -n $i"@%h" -l $LOG_LEVEL -c ${Worker[$i]} -f $LOG_PATH &
    done
    
    sleep 5
    echo "Start beat worker"
    # celery -A $APP beat -l $LOG_LEVEL_BEAT &
    celery -A $APP beat -l $LOG_LEVEL_BEAT -f $LOG_PATH_BEAT &
    source deactivate
}

# Function that kill all celery process & monitoring
stop() {
    pkill -9 -f 'celery'
    pkill -9 -f 'flower'
}

# Function that restart all celery process (stop them then start)
restart() {
    stop
    start
}

case $1 in
  start|stop|restart) "$1" ;;
esac
