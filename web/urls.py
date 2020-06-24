from web.views import WebView
from django.urls import path
from django.conf.urls import include
from django.conf.urls import url


web_view = WebView()

# admin.autodiscover()
urlpatterns = [
    path('index/', web_view.index),
    url('^$', web_view.index),
    path('test/', web_view.test),
    path('register/', web_view.register),
    path('login/', web_view.login),
    path('get_captcha/', web_view.get_captcha),
]
