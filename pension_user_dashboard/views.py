from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile, BookVerification, UserServiceStatus, UserAccountDetails, UserWalletDetails
from pension_user_authentication.models import UserAccountDetails
from .serializers import ( UserProfileSerializer, UserBookVerificationSerializer,
    UserServiceStatusSerializer, UserWalletDetailsSerializer
)


# View for User Home
class PensionUserHome(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        user = self.request.user
        user1 = UserProfile.objects.filter(user = user)
        print(user1)
        return UserProfile.objects.filter(user = user)

    def get(self, request):
        data = {}
        user = request.user
        data['user'] = user.username
        return Response(data, status=status.HTTP_200_OK)
        

# View for User service status 
class PensionUserStatus(generics.GenericAPIView):
    serializer_class = UserServiceStatusSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = UserServiceStatusSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = UserServiceStatus.objects.create(
                user = request.user,
                service_status = serializer.validated_data['service_status'],
            )
            user.save()
            data['message'] = 'Service status added'
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)


# View  for User Profile Completion and Update and Display.
class PensionUserProfile(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_class = (IsAuthenticated,)

    def get(self, request):       
        user = UserProfile.objects.get(user = request.user)
        username = User.objects.get(username = request.user)
        phone_number = UserAccountDetails.objects.get(user = request.user)
        service_status = UserServiceStatus.objects.get(user = request.user)

        data={}
        account_data = {}

        data['username'] = username.username
        data['email'] = username.email
        data['phone_number'] = phone_number.phone_number
        data['Image'] = str(user.Image)
        data['DOB'] = user.DOB
        data['Address'] = user.Address
        data['LGA'] = user.LGA
        data['Name_of_Next_of_Kln'] = user.Name_of_Next_of_Kln
        data['Next_of_Kln_email_address'] = user.Next_of_Kln_email_address
        data['Next_of_Kln_phone'] = user.Next_of_Kln_phone
        data['Next_of_Kln_address'] = user.Next_of_Kln_address

        account_data['service_status'] = service_status.service_status

        return Response({"Basic Information " : data, "Account Information" : account_data }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserProfileSerializer(data = request.data)
        data = {}
        if serializer.is_valid():
            user = UserProfile.objects.create(
            user = request.user,
            DOB = serializer.validated_data['DOB'],
            Address = serializer.validated_data['Address'],
            LGA = serializer.validated_data['LGA'], 
            Name_of_Next_of_Kln = serializer.validated_data['Name_of_Next_of_Kln'],
            Next_of_Kln_email_address = serializer.validated_data['Next_of_Kln_email_address'],
            Next_of_Kln_phone = serializer.validated_data['Next_of_Kln_phone'],
            Next_of_Kln_address = serializer.validated_data['Next_of_Kln_address'],
            )
            user.save()
            data['message'] = 'fields added sucessfuly'
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = UserProfile.objects.get(user = request.user)
        data = {}
        serializer = UserProfileSerializer(user, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            data['message'] = 'profile updated sucessfully'
            return Response(data)   
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


# View for Book verification
class PensionUserBookVerification(generics.GenericAPIView):
    serializer_class = UserBookVerificationSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = UserBookVerificationSerializer(data = request.data)
        data = {}
        user_balance = UserWalletDetails.objects.get(user = request.user)
        balance = user_balance.balance
        if balance < 100:
            data['message'] = 'Book verification Failed, Insufficient account balance'
        else:
            new_balance = balance - 100
            user_balance.balance = new_balance
            user_balance.save()
            if serializer.is_valid():
                user = BookVerification.objects.create(
                    user = request.user,
                    Date = serializer.validated_data['Date'],
                )
                user.save()
                data['message'] = 'Book verification sucessfully done!'
            else:
                data = serializer.errors
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data, status=status.HTTP_200_OK)


# checking wallet balance
class WalletBalanceView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserWalletDetailsSerializer

    def get(self, request):
        data = {}
        try:
            user = UserWalletDetails.objects.get(user = request.user)
            data['balance'] = user.balance
            return Response(data, status = status.HTTP_200_OK)
        except:
            data['message'] = 'Wallet not activated! Please activate your account'
            return Response(data, status = status.HTTP_400_BAD_REQUEST)
