from rest_framework import serializers
from .models import UserProfile, BookVerification, UserServiceStatus, UserWalletDetails


# Serializer for Employe Service Status
class UserServiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserServiceStatus
        fields = ('service_status',)


# Serializer for User Profile Completion and Update.
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'Image', 'DOB', 'Address', 'LGA', 'Name_of_Next_of_Kln', 'Next_of_Kln_email_address',
        'Next_of_Kln_phone', 'Next_of_Kln_address')


# Serializer for User Book Verification
class UserBookVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookVerification
        fields = ('Date',)  


class UserWalletDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWalletDetails
        fields = ('balance',)
