### Repository structure

* `leadgen_api_v1`: Restful API implemented with Django and Django
  Rest Framework.
* `travel_options_updater` Background periodic tasks scheduled and run
  by celery.

### Requirements

* python3 (>= 3.4)
* pip3

### Setup

```shell
$ apt-get install python3-pip
$ apt-get install rabbitmq-server
$ apt-get install libmysqlclient-dev
$ apt-get install gunicorn3
$ apt-get install nginxs

$ cd /path/to/leadgen_source_root/
$ pip3 install -r requirements.txt
```

### Start web service for development

```shell
$ cd /path/to/leadgen_source_root/leadgen_api_v1

$ python3 manage.py makemigrations personalized_options
$ python3 manage.py migrate
$ python3 runserver 0:8000
```

To run test:
```shell
$ python3 manage.py test
```

### Start web service in production

First replace `settings.py` with the file for production settings,
and put configuration file `my.conf` for MySQL under
`/path/to/leadgen_source_root/leadgen_api_v1`.
Then run:

```shell
$ cd /path/to/leadgen_source_root/leadgen_api_v1

$ python3 manage.py makemigrations personalized_options
$ python3 manage.py migrate
$ python3 manage.py collectstatic
$ chmod +x run_gunicorn.sh
$ run_gunicorn.sh
```

Then setup nginx for LeadGen:
```shell
$ cd /path/to/leadgen_source_root/leadgen_api_v1
$ cp leadgen-nginx.conf /etc/nginx/site-available
$ ln -s /etc/nginx/site-available/leadgen-nginx.conf /etc/nginx/site-enabled
```


### Start celery task

```shell
$ cd /path/to/leadgen_source_root/travel_options_updater

$ chmod +x run_updater_combined.sh
$ run_updater_combined.sh
```

### Access admin page

Visit: `http://server_ip:8000/admin`

In admin page, you can see the data stored in LeadGen database and
manage users/groups/tokens, etc.

To create an admin user and api token for the user:

```shell
$ cd /path/to/leadgen_source_root/leadgen_api_v1

$ python3 manage.py createsuperuser
$ python3 manage.py drf_create_token <username>
```
