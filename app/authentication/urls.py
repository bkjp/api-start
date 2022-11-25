from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
    path("login/tokens/", views.MyTokenObtainPairView.as_view(), name = "tokens"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name = "token-refresh"),
    path("login/token/verify/", TokenVerifyView.as_view(), name = "token-verify"),
]