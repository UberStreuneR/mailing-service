from django.contrib import admin
from django.urls import path
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('clients', views.ClientViewSet, basename='client')


urlpatterns = [
    # path('clients/', views.ClientViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    #     'put': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # }), name='clients'),
    path('mailings/', views.MailingViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('mailing-detail/<int:pk>', views.MailingDetailView.as_view()),
    path('messages/', views.MessageViewSet.as_view({
        'get': 'list',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    # path('projects/', views.ProjectViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create',
    #     'put': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # }))
]

urlpatterns += router.urls