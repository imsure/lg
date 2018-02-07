#!/bin/bash

python3 manage.py collectstatic
gunicorn3 --workers=2 -b unix:/home/ubuntu/lg/leadgen_api_v1/leadgen.sock leadgen.wsgi
