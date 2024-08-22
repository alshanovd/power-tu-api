from django.urls import re_path
from analysis import views

urlpatterns = [
    re_path(r'^products/$', views.productsApi),
    re_path(r'^products/([0-9]+)$', views.productsApi),
    re_path(r'^countries/$', views.countriesApi),
    re_path(r'^orders/$', views.ordersApi),
    re_path(r'^annual-revenue/(?P<country>[\w-]+)/$', views.annualRevenueApi),
    re_path(r'^annual-revenue-by-gender/(?P<country>[\w-]+)/$', views.annualRevenueByGenderApi),
    re_path(r'^order-status-count/(?P<country>[\w-]+)/$', views.orderStatusCountApi),
    re_path(r'^total-items-sold/(?P<country>[\w-]+)/$', views.totalItemsSoldApi),
    re_path(r'^statuses-by-month/(?P<country>[\w-]+)/$', views.statusesByMonths),
]
