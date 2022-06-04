from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from .models import Mailing, Client, Message
from .tasks import designate_messages


@receiver(post_save, sender=Mailing)
def create_mailing_message_tasks(sender, instance, created, *args, **kwargs):
    if created:
        designate_messages.delay(instance.id)
        
        
