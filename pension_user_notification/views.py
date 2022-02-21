from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserNotification
from .serializers import NotificationSendSerializer


# View for Send Notification
class PensionUserNotificationSend(APIView):
    serializer_class = NotificationSendSerializer

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user= serializer.data['user']
                username = User.objects.get(id=user).username
                channel_layer = get_channel_layer()
                notification = serializer.data['notification']
                notification_objs = UserNotification.objects.filter(is_seen=False, user= user).count()
                data = {'count':notification_objs,'current_notifications':notification}
                async_to_sync(channel_layer.send)
                (
                    username,{
                        'type':'send_notification',
                        'value':data
                             }
                )
        except:
            data= serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)


# View forReceive Notification
class PensionNotificationReceive(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        username = request.user.username
        channel_layer = get_channel_layer()
        try:
            notification = async_to_sync(channel_layer.receive)(username)
            print(notification)
        except Exception as e:
            print(e)
        return Response(notification, status=status.HTTP_200_OK)



# View for Display notification
class ShowNotification(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        data ={}
        try:
            count = UserNotification.objects.filter(user = request.user.id).count()
            if count > 0 :
                data = UserNotification.objects.filter(user = request.user.id)
                notification = []
                
                for item in data:
                    notification.append(item.notification)

                return Response({"user" : request.user.username, "count" : count, "Notifications" : notification}, status=status.HTTP_200_OK)
            else:
                data['message'] = 'No notifications to display'
                return Response(data, status=status.HTTP_200_OK)
        except:
            data['message'] = 'No notifications to display'
            return Response(data, status=status.HTTP_200_OK)
