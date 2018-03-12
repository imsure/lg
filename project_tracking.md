# Version-1 Checklist

item              | status 
----------------- | --------------------------------------------
Development       | Done
Production        | In operation, Stable, under active testing
Web API           | Django + Django Rest Framework
DB                | MySQL
Background tasks  | Celery Beat
Deployment        | Nginx + Gunicorn on a EC2 T2 Medium instance
Performance       | On avg about 16-17ms to retrieve travel options for a single time slot (online service)


# Problems with Version-1 (priority: high - low)

- Updater not scalable. It uses a bring-all-in-then-update-sequentially scheme. 
  - about 1 sec to update Parade & OTP options for a single entry
  - about 1.5 sec to update Uber options for a single entry

- dev and production env not configurable

- deployment should be completely automated

- the map from timezone to city (otp router) won't work if there are multiple cities within one timezone


# Plan for Version-2 (priority: high - low)

- Make Updater scalable (multiple celery workers, request_future, Amazon Lambda)

- Make dev and production env configurable and automated

- Automate deployment/Wrap everything into virtual env

- Visualize performance data with Periscope

- support for Jenkins/Travis?


# Tasks breakdown for Version-2

Category          | Tasks
----------------- | --------------------------------------------
Scale Updater     | Look into how to scale celery tasks
Scale Updater     | Support query travel option entries by range of slot id in API