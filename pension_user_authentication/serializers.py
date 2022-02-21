from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . models import UserAccountDetails
from .email_sms_code import otp_by_sms, otp_by_email, resend_otp_by_email
import math, random
from django.contrib.auth import authenticate

# Serializer for User Registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'phone_number' )
        extra_kwargs = {
            'password' : {'write_only' : True},
            'confirm_password' : {'write_only' : True}
        }
       
    # validating all fields
    def validate(self, attrs):
        email = attrs.get('email', '')
        phone_number = attrs.get('phone_number', '')
        password = attrs.get('password', '')
        confirm_password = attrs.get('confirm_password', '')
        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({'email' : ('email  is already registered')})
        if len(phone_number) != 13:
            raise serializers.ValidationError({'phone_number' : ('phone_number  is not valid')})
        if password != confirm_password:
            raise serializers.ValidationError({'password' : ('password mismatch, please enter same password')})
        return super().validate(attrs)
        
        
    def create(self, validated_data):        
        # Function to generate OTP
        def generateOTP() :
            digits = "1234567890"
            OTP = ""
            for i in range(5) :
                OTP += digits[math.floor(random.random() * 10)]
            return OTP
        OTP = generateOTP()

        user = User.objects.create(
           username = validated_data['username'],
           email =validated_data['email'],
            )

        userreg = UserAccountDetails.objects.create(
            user = user,
            phone_number = validated_data['phone_number'],
            otp = OTP,
            )

        user.set_password(validated_data['password'])
        user.is_active = False

        # Calling function to send otp using  email
        otp_by_email(validated_data['email'], OTP)
        # Calling function to send otp using sms
        otp_by_sms(validated_data['phone_number'], OTP)

        user.save()
        userreg.save()
        return user


# Serializer for Resend OTP Verification
class ResendOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validat(self, attrs):
        email = attrs.get('email', '')
        if not User.objects.filter(email = email).exists(): 
            raise serializers.ValidationError({'email' : ('email is not registered')})
    
    def create(self, validated_data):
        def generateOTP() :
            digits = "1234567890"
            OTP = ""
            for i in range(5) :
                OTP += digits[math.floor(random.random() * 10)]
            return OTP
        OTP = generateOTP()
        user = User.objects.get(email = validated_data['email'])
        userreg = UserAccountDetails.objects.get(user = user)
        userreg.otp = OTP
        
        # Calling function to send otp using  email

        resend_otp_by_email(validated_data['email'], OTP, user.username)

        userreg.save()
        return user


# Serializer for Account Activation
class AccountActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccountDetails
        fields = ('otp',)

    def create(self, validated_data):
        try:
            user = UserAccountDetails.objects.get(otp = validated_data['otp'])
            
            if user:
                user.is_active = True
                user.save()
                return user
        except:
            raise serializers.ValidationError({'message' : ('Entered OTP is invalid!!Please enter the correct OTP.')})
        

# Serializer for Token generation by extending TokenObtainPairSerializer
class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(UserLoginSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({'message':
                ('A user with this email and password is not found.')}
            )

        return super().validate(attrs)


# Serializer for Change Password
class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

