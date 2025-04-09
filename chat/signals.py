# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .tasks import send_email_async

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Our Platform!"
        message = f"Hello {instance.username},\n\nThank you for registering."
        recipient_list = [instance.email]
        
        # Call the Celery task to send the email asynchronously
        send_email_async.delay(subject, message, recipient_list)
