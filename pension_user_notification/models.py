from django.db import models
from django.contrib.auth.models import User


# Modle for User Notification
class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    notification = models.TextField(max_length = 100)
    is_seen = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-notification']
        