from django.contrib.auth.models import User
from django.db import models


#Model for User Registration 
class UserAccountDetails(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    phone_number = models.CharField(max_length = 13, null = False, blank = False)
    otp = models.CharField(max_length = 5)
    is_active = models.BooleanField(default = False) 
    
    def __str__(self):
        return self.user.username


from django.core.mail import send_mail  
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.conf import settings

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "token = " + reset_password_token.key
   
    send_mail(
        # title:
        "Password Reset ",
        # message:
        email_plaintext_message,
        # from:
        settings.EMAIL_HOST_USER,
        # to:
        [reset_password_token.user.email]
    )
