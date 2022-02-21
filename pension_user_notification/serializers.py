from rest_framework import serializers
from .models import UserNotification

# Serializer for Notification send
class NotificationSendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ('user', 'notification',)
