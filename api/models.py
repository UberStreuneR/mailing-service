from django.db import models
from django.core.validators import MinLengthValidator
from django_celery_beat.models import PeriodicTask
from django.utils import timezone
import pytz
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask, IntervalSchedule


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
MESSAGES_STATUSES = (
    ('S', 'Sent'),
    ('P', 'Pending'), 
    ('E', 'Error'),
    ('U', 'Uninitiated')
)
# Create your models here.


class Client(models.Model):
    number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    operator_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)], blank=True, null=True)
    tag = models.CharField(max_length=5)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Moscow')

class Mailing(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    message = models.CharField(max_length=150, null=True, blank=True)
    filter_operator_code = models.CharField(max_length=3, null=True, blank=True)
    filter_tag = models.CharField(max_length=5, null=True, blank=True)
    enabled = models.BooleanField(default=True)

    # def save(self, *args, **kwargs):
    #     run_mailings_task = PeriodicTask.objects.get_or_create(name="Run mailings")
    #     super(Mailing, self).save(*args, **kwargs)

class Message(models.Model):
    sent_time = models.DateTimeField(blank=True)
    status = models.CharField(max_length=1, choices=MESSAGES_STATUSES, default='U')
    client_id = models.IntegerField(blank=True, null=True)
    parent_mailing = models.ForeignKey(Mailing, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)
    error = models.CharField(max_length=200, blank=True)


# class Project(models.Model):
#     project_name = models.CharField(max_length=200, unique=True)
#     project_scan = models.IntegerField()  
#     project_status = models.BooleanField()

#     def set_periodic_task(self, task_name):
#         schedule = self.get_or_create_interval()
#         PeriodicTask.objects.create(
#             interval=schedule, 
#             name=f'{self.project_name}-{self.id}', 
#             task='api.tasks.run_mailings',
#         )

#     def get_or_create_interval(self):
#         schedule, created = IntervalSchedule.objects.get_or_create(
#             every=self.project_scan,
#             period=IntervalSchedule.SECONDS,
#         )
#         return schedule

#     def get_periodic_task(self, task_name):
#         interval = self.get_or_create_interval()
#         periodic_task = PeriodicTask.objects.get(
#             interval=interval, 
#             name=f'{self.project_name}-{self.id}', 
#             task=task_name,
#         )
#         return periodic_task

#     def sync_disable_enable_task(self, task_name):
#         periodic_task = self.get_periodic_task(task_name)
#         periodic_task.enabled = self.project_status
#         periodic_task.save()


# @receiver(post_save, sender=Project)
# def set_or_sync_periodic_task(sender, instance=None, created=False, **kwargs):
#     if created:
#         instance.set_periodic_task(task_name='api.tasks.run_mailing')
#     else:
#         instance.sync_disable_enable_task(task_name='api.tasks.run_mailing')
