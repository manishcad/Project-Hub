from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_page, name="Login"),
    path("signup", views.signup, name="Signup"),
    path("account_edit", views.account_edit, name="Account_edit"),
    path("signout", views.signout, name="Singout"),
    path("User_Profile/<str:pk>", views.User_Profile, name="Profile"),
    path("Forgot_password", views.forgot_password, name="Forgot_password"),
    path("Change_passsword/<str:pk>",
         views.change_password, name="Change_password"),
    path("Password_sent", views.password_sent, name="Password_sent"),
    path("Follow/<str:pk>", views.follow, name="Follow"),
]
