# django gunicorn script
# Generates a Daemon process with Gunicorn.
# see processes with ps -aux
# tested on: Ubuntu 14.04.3 LTS (GNU/Linux 3.13.0-74-generic x86_64), aws ec2
# Runs on apps built with Django==1.9
# Marcus Shepherd <marcusshepdotcom@gmail.com>
# 3-12-16


NAME=trans # REPLACE WITH BASE DIR NAME


SETTINGS=$NAME.settings
SOCK=/home/1/trans/proc/$NAME-gunicorn.sock
PID=/home/1/trans/proc/$NAME-gunicorn.pid
#LOGFILE=/home/trans/logs/$NAME-gunicorn.log
WORKERS=3


echo 'Creating Daemon process for: '$NAME
#echo 'LOGFILE: '$LOGFILE

# this is where .sock .log and .pid get put
DIRECT=/home/1/trans/proc
if ! [ -d $DIRECT ]; then
    ls -la /home/1/trans/
    echo $DIRECT" does not exist.. creating.."
    sudo mkdir $DIRECT
    ls -la /home/1/trans/
else
    echo "Yes it does."
    echo "removing /opt/proc/$NAME*"
    rm -rf /home/1/trans/proc/$NAME*
fi


exec /home/1/trans/venv/bin/gunicorn \
    --env DJANGO_SETTINGS_MODULE=$SETTINGS \
    $NAME.wsgi:application \
    --pid $PID \
    --bind unix:$SOCK \
    --workers $WORKERS \
    --name $NAME \
 #   --daemon \
 #   --log-file=$LOGFILE

# run from /opt/project
