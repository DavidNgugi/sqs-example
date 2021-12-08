# SQS Example

Playing with SQS, Boto3 and Celery in Python 3

## Setting Up Enviornment

`NOTE`: You can use this up with docker or run with by setting up your virtual environment. 
If you don't have `virtualenv`, install it by running:

```sh
pip install virtualenv
```

Create the virtual environment

```sh
virtualenv sqs-example
```

Activate the virtual environment

```sh
source sqs-example/bin/activate
```

## Running local SQS service on docker

Listens on port `9324` and accessible on your browser at [http://localhost:9325/](http://localhost:9325/)

```
docker compose up -d
```

## Install packages locally

Set celery configs and install your packages

```sh
cp celery/settings.cfg.example celery/settings.cfg && pip install -r requirements.txt
```

## Test Simple SQS example withour Celery

```sh
python3 main.py
```
## Test Simple Celery with SQS example

```sh
python3 celery_app.py
```