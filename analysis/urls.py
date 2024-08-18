from django.urls import re_path, path
from analysis import views

urlpatterns = [
    re_path(r'^products/$', views.productsApi),
    re_path(r'^products/([0-9]+)$', views.productsApi),
    path('order-items/', views.OrderItemsListView.as_view(), name='order-items'),

]

