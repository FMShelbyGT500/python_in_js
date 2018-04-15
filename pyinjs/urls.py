from django.conf.urls import url
from . import views

app_name = "pyinjs"

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^handling_post_request$', views.hpr, name='handling_post_request'),
]
