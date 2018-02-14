#!/bin/bash

celery -A updater worker -B --loglevel=INFO -f /home/ubuntu/leadgen_updater.log
