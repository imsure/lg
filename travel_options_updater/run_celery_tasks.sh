#!/bin/bash

celery -A updater worker -B
