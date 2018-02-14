#!/bin/bash

celery -A parade_otp_updater worker -B --loglevel=INFO -f /home/ubuntu/parade_otp_updater.log
