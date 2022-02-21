from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client


# Function to send OTP through email
def otp_by_email(email, otp):
    send_mail(
        subject = 'Account Verification Code',
        message = 'Your Account verification OTP sended sucessfully. Use OTP to verify the account:'+ otp,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=True,
            )   
       

# Function to resend OTP through email
def resend_otp_by_email(email, otp, username):
    send_mail(
        subject = 'Account Verification Code',
        message = 'Hi  '+  username  +',Please enter the following verification code to access your Account.'+otp,
        from_email = settings.EMAIL_HOST_USER,
        recipient_list=[email, ],
        fail_silently=True,
            )   
     

# Function to send OTP through sms
def otp_by_sms(phone_number, otp):
    account = settings.TWILIO_ACCOUNT_SID
    token = settings.TWILIO_AUTH_TOKEN
    client = Client(account, token)
    message = client.messages.create(
    body = f'Your Account verification OTP sended sucessfully. Use OTP to verify the account.'+otp,
    from_ = settings.TWILIO_FROM_,
    to = phone_number
    )
