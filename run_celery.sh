#!/bin/bash

# Run Redis server (if not already running)
redis-server &

# Wait for Redis to start
sleep 2

# Change to project directory
cd Dramoir

# Run Celery worker
celery -A MovieSeries worker -l info 