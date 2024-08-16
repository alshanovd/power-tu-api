from django.urls import re_path
from analysis import views

urlpatterns = [
    re_path(r'^products/$', views.Home.as_view()),
    re_path(r'^products/([0-9]+)$', views.Home.as_view()),
]
