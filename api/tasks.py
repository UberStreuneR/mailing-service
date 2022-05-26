from __future__ import absolute_import, unicode_literals
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from celery import shared_task
from django.utils import timezone
import requests
import json
from .models import Mailing, Client, Message


API_URL = "https://probe.fbrq.cloud/v1/send/"
headers = {
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODUwMjg1NjAsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im9sZWcuc3RldHN1ayJ9.CmQqDWeRuMsD_9MMX3hJ7pAXIpSxytNkIUSTFP618FM"
}

run_mailings_task = PeriodicTask.objects.filter(enabled=True).first()
@shared_task
def run_mailings():
    mailings = Mailing.objects.filter(enabled=True)
    if mailings.count() == 0:
        run_mailings_task.enabled = False
        run_mailings_task.save()
        return
    for mailing in mailings:
        if timezone.now() > mailing.end_time:
            mailing.enabled = False
            mailing.save()
            continue
        if timezone.now() > mailing.start_time and timezone.now() < mailing.end_time:
            clients = Client.objects.filter(tag=mailing.filter_tag, operator_code=mailing.filter_operator_code)
            for client in clients:
                message = Message.objects.create(sent_time=timezone.now(), client_id = client.id, parent_mailing = mailing)

                request_data = {
                    "id": message.id,
                    "phone": int(client.number),
                    "text": mailing.message
                }
                r = requests.post(API_URL + str(message.id), data=request_data, headers=headers)
                if r.status_code == 200:
                    message.status = 'S'
                    message.error = r.content
                elif r.status_code >= 400 and r.status_code < 500:
                    message.status = 'E'
                    message.error = r.content
                elif r.status_code >= 500:
                    return
                message.save()
            mailing.enabled = False
        mailing.save()