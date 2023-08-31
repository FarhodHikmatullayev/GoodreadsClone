from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, *args, **kwargs):
    if created:
        send_mail(
            subject='Welcome to our site',
            message='akacha akacha akacha',
            from_email='farhodjonhikmatullayev@gmail.com',
            recipient_list=[instance.email]
        )


# post_save.connect(send_welcome_email, sender=User)
