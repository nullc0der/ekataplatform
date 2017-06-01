#!/bin/bash
while ! pg_isready -h $DJANGO_DATABASE_HOST -p "5432" > /dev/null 2> /dev/null; do
   echo "Connecting to postgres Failed"
   sleep 1
done
python manage.py migrate
python manage.py collectstatic --noinput
circusd circus.ini
