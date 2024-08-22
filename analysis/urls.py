from django.urls import re_path
from analysis import views

urlpatterns = [
    re_path(r'^products/$', views.productsApi),
    re_path(r'^products/([0-9]+)$', views.productsApi),
    re_path(r'^countries/$', views.countriesApi),
    re_path(r'^orders/$', views.ordersApi),
    re_path(r'^annual-revenue/$', views.annualRevenueApi),
    re_path(r'^annual-revenue-by-gender/$', views.annualRevenueByGenderApi),
    re_path(r'^order-status-count/$', views.orderStatusCountApi),
    re_path(r'^total-items-sold/$', views.totalItemsSoldApi),
    re_path(r'^statuses-by-month/(?P<country>[\w-]+)/$', views.statusesByMonths),
]
