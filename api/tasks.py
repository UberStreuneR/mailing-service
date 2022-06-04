from __future__ import absolute_import, unicode_literals
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task
from mailing.celery import app
from django.utils import timezone
import requests
import json
import pytz, datetime
from .models import Mailing, Client, Message




API_URL = "https://probe.fbrq.cloud/v1/send/"
headers = {
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODUwMjg1NjAsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im9sZWcuc3RldHN1ayJ9.CmQqDWeRuMsD_9MMX3hJ7pAXIpSxytNkIUSTFP618FM"
}

@app.task
def designate_messages(mailing_id):
    mailing = Mailing.objects.get(pk=mailing_id)
    start_time = mailing.start_time
    end_time = mailing.end_time
    clients = Client.objects.filter(tag=mailing.filter_tag, operator_code=mailing.filter_operator_code)
    if timezone.now() < end_time: # if there is some time left until the mailing ends
        for client in clients:
            clients_time = datetime.datetime.now(pytz.timezone(client.timezone)).replace(tzinfo=pytz.timezone("UTC")) #20:00MSK -> 20:00UTC
            print(clients_time, start_time, clients_time > start_time, start_time - clients_time)
            if clients_time > start_time: # if it's 20:00UTC, then if clients_time is > 20:00MSK, send immediately
                create_message.apply_async((client.id, mailing.id))
            else: # if start_time is 20:00UTC and clients_time is 19:00MSK, send in one hour
                create_message.apply_async((client.id, mailing.id), eta=timezone.now() + (start_time - clients_time))
    return timezone.now(), start_time


@app.task
def create_message(client_id, parent_mailing_id):
    parent_mailing = Mailing.objects.get(pk=parent_mailing_id)
    Message.objects.create(sent_time=timezone.now(), client_id = client_id, parent_mailing=parent_mailing)


# @app.task
# def run_mailings():
#     mailings = Mailing.objects.filter(enabled=True)
#     if mailings.count() == 0:
#         # if run_mailings_task:
#         #     run_mailings_task.enabled = False
#         #     run_mailings_task.save()
#         return
#     for mailing in mailings:
#         if timezone.now() > mailing.end_time:
#             mailing.enabled = False
#             mailing.save()
#             continue
#         if timezone.now() > mailing.start_time and timezone.now() < mailing.end_time:
#             clients = Client.objects.filter(tag=mailing.filter_tag, operator_code=mailing.filter_operator_code)
#             for client in clients:
#                 message = Message.objects.create(sent_time=timezone.now(), client_id = client.id, parent_mailing = mailing)

#                 request_data = {
#                     "id": message.id,
#                     "phone": int(client.number),
#                     "text": mailing.message
#                 }
#                 # r = requests.post(API_URL + str(message.id), data=request_data, headers=headers)
#                 # if r.status_code == 200:
#                 #     message.status = 'S'
#                 #     message.error = r.content
#                 # elif r.status_code >= 400 and r.status_code < 500:
#                 #     message.status = 'E'
#                 #     message.error = r.content
#                 # elif r.status_code >= 500:
#                 #     return
#                 # message.save()
#             mailing.enabled = False
#         mailing.save()