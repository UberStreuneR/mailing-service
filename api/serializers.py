from rest_framework import serializers
from .models import Mailing, Client, Message




class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MailingSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model = Mailing
        fields = '__all__'


class MailingStatsSerializer(serializers.ModelSerializer):
    messages_failed_queryset = Message.objects.filter(status='E')
    messages_success_queryset = Message.objects.filter(status='S')
    messages_uninitialized_queryset = Message.objects.filter(status='U')
    # messages = MessageSerializer(many=True)
    messages_failed = MessageSerializer(messages_failed_queryset, many=True, read_only=True)
    messages_success = MessageSerializer(messages_success_queryset, many=True, read_only=True)
    messages_uninitialized = MessageSerializer(messages_uninitialized_queryset, many=True, read_only=True)

    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'filter_operator_code', 'filter_tag', 'messages_failed', 'messages_success', 'messages_uninitialized']


# class ProjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Project
#         fields = '__all__'