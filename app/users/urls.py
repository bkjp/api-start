from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView,TokenVerifyView


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name = "user-register"),
    path("register-verifcation/", views.RegisterEmailVerification.as_view(), name = "register-verification"),

    path("me/", views.LoadUserView.as_view(), name = "user"),
    path("all/", views.GetUsers.as_view(), name = "users"),

    path("update/", views.UpdateUserView.as_view(), name = "user-update"),

    path("single/delete/", views.DeleteUserView.as_view(), name = "user-delete"),
    path("delete/all/", views.DeleteAllUserView.as_view(), name = "users-delete"),
]