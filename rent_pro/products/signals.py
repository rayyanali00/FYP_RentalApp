from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from notifications.signals import notify


@receiver(post_save, sender=Order)
def create_order(sender, instance, created, **kwargs):
    if created:
        print(instance)
        # notify.send(user, recipient=user, verb='you reached level 10')
