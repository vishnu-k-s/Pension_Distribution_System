from django.urls import path, include
from . views import (PensionUserLogin, PensionUserRegister,PensionUserActivation, PensionUserLogin,
    PensionUserChangePassword, PensionResendOTP, 
    )


urlpatterns = [
    path('user-register/', PensionUserRegister.as_view(), name = 'user-register'),
    path('resend-otp/', PensionResendOTP.as_view(), name = 'resend-otp'),
    path('user-activation/', PensionUserActivation.as_view(), name = 'user-activation'),
    path('user-login/', PensionUserLogin.as_view(), name='user-login'),  
    path('password-reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/change-password/', PensionUserChangePassword.as_view(), name='change-password'),
]
