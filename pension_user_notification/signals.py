from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from pension_user_dashboard.models import BookVerification
from pension_user_notification.models import UserNotification


@receiver(post_save, sender=BookVerification)
def save_notification(sender, instance, created, **kwargs):  
    if created:
        user  = User.objects.get(username = instance)
        notification = 'Appointment booked on ' + str(instance.Date) 
        UserNotification.objects.create(user=user, notification=notification)
