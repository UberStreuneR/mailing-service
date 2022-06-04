from django.http import JsonResponse, Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import MailingSerializer, MailingStatsSerializer, ClientSerializer, MessageSerializer
from .models import Mailing, Client, Message
from api import serializers
from django.views import View
from django.utils import timezone
import requests
from datetime import datetime
# Create your views here.


# class ProjectViewSet(viewsets.ModelViewSet):
#     serializer_class = ProjectSerializer
#     queryset = Project.objects.all()


# class ClientViewSet(viewsets.ModelViewSet):
#     serializer_class = ClientSerializer
#     queryset = Client.objects.all()

#     def get_object(self, pk):
#         obj = self.queryset.get(pk=pk)
#         return obj

class ClientViewSet(viewsets.ViewSet):
    def list(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def update(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        serializer = ClientSerializer(instance=client, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        client = Client.objects.get(pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MailingViewSet(viewsets.ModelViewSet):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        datetime_template = "%Y-%m-%d %H:%M:%S"
        start_time=data['start_time']
        end_time=data['end_time']
        start_date = datetime.strptime(start_time, datetime_template)
        end_date = datetime.strptime(end_time, datetime_template)
        mailing = Mailing.objects.create(start_time=start_date, end_time=end_date, message=data['message'], filter_tag=data['filter_tag'], filter_operator_code=data['filter_operator_code'])
        
        # project = Project.objects.get_or_create(project_name="Run mailings", project_scan=10, project_status=True)
        
        return Response(self.serializer_class(mailing).data)


class MailingDetailView(APIView):

    def get_object(self, pk):
        try:
            return Mailing.objects.get(pk=pk)
        except Mailing.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mailing_object = self.get_object(pk)
        serializer = serializers.MailingStatsSerializer(mailing_object)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()


    # def create(self, request, *args, **kwargs):
    #     data = request.data
    #     clients = Client.objects.filter(id__in=data['clients'])
    #     mailing = Mailing.objects.create(start_time=data['start_time'], end_time=data['end_time'], message=data['message'], filter=data['filter'])
    #     mailing.clients.set(clients)
    #     return Response(self.serializer_class(mailing).data)

API_URL = "https://probe.fbrq.cloud/v1/send/"
headers = {
    'Authorization': "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODUwMjg1NjAsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Im9sZWcuc3RldHN1ayJ9.CmQqDWeRuMsD_9MMX3hJ7pAXIpSxytNkIUSTFP618FM"
}

class TestView(APIView):

    def get(self, *args, **kwargs):
        client = Client.objects.first()
        mailing = Mailing.objects.first()
        
        request_data = {
                    'id': client.id,
                    'phone': int(client.number),
                    'text': mailing.message
                }
        message = Message.objects.create(sent_time=timezone.now(), client_id = client.id, parent_mailing = mailing)
        print(API_URL + str(message.id), request_data, headers)
        r = requests.post(API_URL + str(message.id), data=request_data, headers=headers)
        print(r.content, r.status_code)
        return Response(r)



# class AddClientView(APIView):

#     def get_object(self, pk):
#         try:
#             return Client.objects.get(pk=pk)
#         except Client.DoesNotExist:
#             raise Http404


#     def post(self, request, format=None):
#         serializer = ClientSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk, format=None):
#         client = self.get_object(pk)
#         serializer = ClientSerializer(client, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, pk, format=None):
#         client = self.get_object(pk)
#         client.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class ClientDetailView(APIView):


#     def get_object(self, pk):
#         try:
#             return Mailing.objects.get(pk=pk)
#         except Mailing.DoesNotExist:
#             raise Http404


#     def post(self, request, format=None):
#         serializer = MailingSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def update(self, request, pk, format=None):
#         mailing = self.get_object(pk)
#         serializer = MailingSerializer(mailing, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, pk, format=None):
#         mailing = self.get_object(pk)
#         mailing.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)