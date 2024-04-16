from django.urls import path
from bar_app.views import auth_view

urlpatterns = [
    path("register/",  auth_view.RegisterUser.as_view(), name="register"),
    path("login/",  auth_view.LoginUser.as_view(), name="login"),
    path("logout/",  auth_view.LogoutUser.as_view(), name="logout"),
]