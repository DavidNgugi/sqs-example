FROM python:3.6

COPY . .

# Fix missing pycurl module error 
# RUN apt-get install -y --no-install-recommends libcurl4-nss-dev libssl-dev

RUN pip install -r requirements.txt

# CMD [ celery_app.py ]