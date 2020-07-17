from resourcemanagement.views import ResourceManagementView
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url

resourcemanagement_view = ResourceManagementView()

urlpatterns = [
    path('getSnmpInfo/', resourcemanagement_view.getSnmpInfo),
    path('host/', resourcemanagement_view.getHost),
    path('problems/', resourcemanagement_view.getProblems),
]
