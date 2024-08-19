from django.urls import path, re_path
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    re_path(r'^register/$', RegisterView.as_view()),
    re_path(r'^login/$', TokenObtainPairView.as_view()),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view()),
]