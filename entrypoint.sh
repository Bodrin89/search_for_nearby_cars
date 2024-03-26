#!/bin/bash -x

python3 manage.py migrate --noinput || exit 1
exec "$@"
