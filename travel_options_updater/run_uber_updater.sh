#!/bin/bash

celery -A uber_updater worker -B --loglevel=INFO -f /home/ubuntu/uber_updater.log
