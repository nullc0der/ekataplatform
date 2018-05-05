#!/bin/sh
while ! pg_isready -h $DJANGO_DATABASE_HOST -p "5432" > /dev/null 2> /dev/null; do
   echo "Waiting for DB host....."
   sleep 1
done
echo "Starting Celery Beat"
/usr/local/bin/celery beat -A ekatadeveloper --loglevel=INFO
