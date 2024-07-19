from django import path
from . import views

urlpatterns = [
    path('powerusers/', views.PowerUserListCreate.as_view(), name='poweruser_list_create'),
]