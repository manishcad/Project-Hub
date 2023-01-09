from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="Index"),
    path("add_project", views.add_project, name="Add_project"),
    path("my_account", views.my_account, name="My_account"),
    path("projects", views.projects, name="Projects"),
    path("single_project/<str:pk>", views.single_project, name="Single_project"),
    path("add_skills", views.add_skills, name="Add_skills"),
    path("delete_skill/<str:pk>", views.delete_skill, name="Delete_skill"),
    path("delete_project/<str:pk>", views.delete_project, name="Delete_project"),
    path("inbox", views.inbox, name="Inbox"),
    path("view_msg/<str:pk>", views.view_msg, name="View_msg"),
    path("send_msg/<str:pk>", views.send_msg, name="Send_msg"),
    path("edit_skill/<str:pk>", views.edit_skill, name="Edit_skill"),
    path("edit_project/<str:pk>", views.edit_project, name="Edit_project"),
    path("Like/<str:pk>", views.like, name="Like"),
]
