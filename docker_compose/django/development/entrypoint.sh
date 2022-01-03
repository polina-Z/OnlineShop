#!/bin/bash
set -e
cmd="$@"

if [ -z "$POSTGRES_USER" ]; then
    export POSTGRES_USER=postgres
fi

# If not DB is set, then use USER by default
if [ -z "$POSTGRES_DB" ]; then
    export POSTGRES_DB=$POSTGRES_USER
fi

# Need to update the DATABASE_URL if using DOCKER
export DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_DB


function postgres_ready(){
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="$POSTGRES_DB", user="$POSTGRES_USER", password="$POSTGRES_PASSWORD", host="postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - continuing..."
exec $cmd
