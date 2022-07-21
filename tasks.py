import os
import configparser

from celery import Celery
from celery.worker.consumer import Consumer
from kombu import Queue

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'celery/settings.cfg'))

app = Celery('tasks', broker=config.get('celery', 'broker'))

def on_unknown_task(self, body, message, exc):
    task_name = message.headers.get('task')
    task_id = message.headers.get('id')
    print(f'[on_unknown_task] Ignoring and acknowledging message for '
          f'unknown task. Task name: {task_name}, Task id: {task_id}')
    message.ack()

Consumer.on_unknown_task = on_unknown_task

app.conf.max_retries = 3

app.conf.task_queues = (
    Queue('skill-assessments.fifo', routing_key='skill-assessments.fifo'),
    Queue('skill-assessments-dead-letter.fifo', routing_key='skill-assessments-dead-letter.fifo'),
)

@app.task(queue='skill-assessments.fifo')
def score_question(x, y):
    print(f"Doing scoring...x: {x}, y: {y}")
    return x + y