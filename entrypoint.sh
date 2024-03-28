#!/bin/bash -x

python3 manage.py migrate --noinput || exit 1

python3 utils/lte_postgres.py || exit 1

python3 manage.py collectstatic --noinput || exit 1

wait
exec "$@"
