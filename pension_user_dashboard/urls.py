from django.urls import path
from . views import(
    PensionUserProfile, PensionUserBookVerification, PensionUserStatus, PensionUserHome, WalletBalanceView
)
urlpatterns = [
    path('user-home/', PensionUserHome.as_view(), name = 'user-home'),
    path('user-profile/', PensionUserProfile.as_view(), name = 'user-profile'),  
    path('book-verification/', PensionUserBookVerification.as_view(), name = 'book-verification'),
    path('service-status/', PensionUserStatus.as_view(), name = 'service-status'),
    path('wallet-balance/', WalletBalanceView.as_view(), name = 'wallet-balance'), 
]
