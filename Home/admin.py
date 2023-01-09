from django.contrib import admin
from .models import Project, Comment, Skill, New_msg, Like
# Register your models here.
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(Skill)
admin.site.register(New_msg)
admin.site.register(Like)
