#!/bin/sh
while ! pg_isready -h $DJANGO_DATABASE_HOST -p "5432" > /dev/null 2> /dev/null; do
   echo "Waiting for DB host....."
   sleep 1
done
echo "Starting daphne server"
daphne -b 0.0.0.0 -p 8000  ekatadeveloper.asgi:channel_layer
