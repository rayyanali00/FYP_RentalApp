from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("login/",auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login" ),
    path("register/",views.RegisterUser.as_view(), name="register" ),
    path("test/",views.Test.as_view(), name="test" ),
    path("logout/",auth_views.LogoutView.as_view(), name="logout" ),
    path("admin_dashboard/",views.AdminDashboard.as_view(), name="admin-dashboard"),
    path("user_list_template/",views.UserListTemplate.as_view(), name="user-list-template"),
    path("user_list/",views.User_List, name="user-list-api"),
    path("user_list_graph_api/",views.User_List_Graph, name="user-list-graph-api"),
]