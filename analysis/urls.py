from django.urls import re_path
from analysis import views

urlpatterns = [
    re_path(r'^products/$', views.productsApi),
    re_path(r'^products/([0-9]+)$', views.productsApi),
    re_path(r'^countries/$', views.countriesApi),
    re_path(r'^orders/$', views.ordersApi),
]
