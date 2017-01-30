#!/bin/bash

NAME=trans
HOMEDIR=/home/alex/
DJANGODIR=${HOMEDIR}/${NAME}
SOCKFILE=/tmp/${NAME}.sock
# Три рабочих процесса на 1 ядро процессора
NUM_WORKERS=3
DJANGO_WSGI_MODULE=${NAME}.wsgi
GUNICORN=${HOMEDIR}/trans/venv/bin/gunicorn

cd $DJANGODIR
source ${HOMEDIR}trans/venv/bin/activate

# Если по какой-то причине директории с SOCKFILE не существует -- создаем её
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Запускаем наш Django-проект
# Опционально можем записывать Debug в лог файлы (или другие файлы)
exec ${GUNICORN} ${DJANGO_WSGI_MODULE}:application \
  --workers $NUM_WORKERS \
  --bind unix:${SOCKFILE} \
# добавляем если настройки проекта хранятся в не стандартном модуле
# --env DJANGO_SETTINGS_MODULE=settings.production \
# --log-level=debug \
# --log-file=-