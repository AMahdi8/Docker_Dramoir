#!/bin/bash
set -e

PG_HOST=${DB_HOST:-db}
PG_USER=${DB_USER:-backend}
PG_DB=${DB_NAME:-movieseries}
DUMP_FILE="/docker-entrypoint-initdb.d/dramoir_backup.dump"

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$PG_HOST" -U "$PG_USER" -d "$PG_DB"; do
  sleep 2
done

echo "Starting database restore..."
pg_restore -h "$PG_HOST" -U "$PG_USER" -d "$PG_DB" -Fc -v "$DUMP_FILE"

echo "Restore completed successfully!"