from django.urls import path

from authentication.views import LoginApi, CreateUser

urlpatterns = [
    path("login/", LoginApi.as_view()),
    path("register/", CreateUser.as_view()),
]
