from django.db import models
from django.contrib.auth.models import User
from pension_user_authentication.models import UserAccountDetails


# Model for UserProfile
class UserProfile(models.Model):

# Function to automatically build file name
    def nameFile(instance, filename):
        return '/'.join(['Images', str(instance.user), filename])

    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Image = models.ImageField(upload_to = nameFile, blank = True, default = 'None')
    DOB = models.DateField(max_length = 8, null = False, blank = False)
    Address = models.TextField(null = False, blank = False)
    LGA = models.CharField(max_length = 50, null = False, blank = False)
    Name_of_Next_of_Kln = models.CharField(max_length = 50, null = False, blank = False)
    Next_of_Kln_email_address = models.EmailField(max_length = 254, null = False, blank = False)
    Next_of_Kln_phone = models.CharField(max_length = 13, null = False, blank = False)
    Next_of_Kln_address = models.CharField(max_length = 50, null = False, blank = False)

    def __str__(self):
        return self.user.username


# Model for Book Verification
class BookVerification(models.Model):
    # user = models.OneToOneField(User, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    Date = models.DateTimeField(max_length = 8, null = False, blank = False)
    is_verified = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username


# Model for Service Status
service_choice = (
        ( "Active","Active"),
        ("Retried", "Retried"),
    )
class UserServiceStatus(models.Model):
    user  = models.OneToOneField(User, on_delete = models.CASCADE)
    service_status = models.CharField(max_length = 10, choices = service_choice, default = None)

    def __str__(self):
        return self.user.username


class UserWalletDetails(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    balance = models.DecimalField(max_digits = 10, decimal_places = 2,default = 0.0)

    def __str__(self):
        return self.user.username

