from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UserAccountDetails

from . serializers import ( UserRegistrationSerializer, AccountActivationSerializer,
        UserLoginSerializer, ChangePasswordSerializer, ResendOTPSerializer,  UserLoginSerializer
    )


# View for User Registration
class PensionUserRegister(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['message'] = " An otp has sent to the phone number and email, Please verify  your account "
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


# View for ResendOTP
class PensionResendOTP(generics.GenericAPIView):
    serializer_class = ResendOTPSerializer

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['message'] = "An otp has sent to the phone number  and verify  your account "
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


# View for Account Activation
class PensionUserActivation(generics.GenericAPIView):
    serializer_class = AccountActivationSerializer

    def post(self, request):
        serializer = AccountActivationSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            user =UserAccountDetails.objects.get(otp = request.data['otp'])
            user_obj =User.objects.get(username = user.user)
            user_obj.is_active = True
            user_obj.save()
            data['message'] = "Your account activated successfully by OTP, Please Login!!"
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


# View for Token generation
class PensionUserLogin(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    

# View for Change Password
class PensionUserChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]})
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            data['message'] = 'Password updated successfully'
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)

