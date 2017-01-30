#!/bin/bash

NAME=trans
HOMEDIR=/home/alex/
DJANGODIR=${HOMEDIR}/${NAME}
SOCKFILE=/tmp/${NAME}.sock
# ��� ������� �������� �� 1 ���� ����������
NUM_WORKERS=3
DJANGO_WSGI_MODULE=${NAME}.wsgi
GUNICORN=${HOMEDIR}/trans/venv/bin/gunicorn

cd $DJANGODIR
source ${HOMEDIR}trans/venv/bin/activate

# ���� �� �����-�� ������� ���������� � SOCKFILE �� ���������� -- ������� �
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# ��������� ��� Django-������
# ����������� ����� ���������� Debug � ��� ����� (��� ������ �����)
exec ${GUNICORN} ${DJANGO_WSGI_MODULE}:application \
  --workers $NUM_WORKERS \
  --bind unix:${SOCKFILE} \
# ��������� ���� ��������� ������� �������� � �� ����������� ������
# --env DJANGO_SETTINGS_MODULE=settings.production \
# --log-level=debug \
# --log-file=-