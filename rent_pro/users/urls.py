from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("login/",auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login" ),
    path("register/",views.RegisterUser.as_view(), name="register" ),
    path("test/",views.Test.as_view(), name="test" ),
    path("logout/",auth_views.LogoutView.as_view(), name="logout" ),
]