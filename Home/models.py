from django.db import models
from User.models import Profile
# Create your models here.


class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="project_images")
    about = models.TextField(blank=True, null=True, default="No Descriptions ")
    source_code = models.URLField(blank=True, null=True)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    msg = models.TextField()

    def __str__(self):
        return self.profile.user.username


class Like(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.project.name)


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=50)
    skill_bio = models.TextField(blank=True)

    def __str__(self):
        return self.skill_name


class New_msg(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="receiver")
    is_read = models.BooleanField(default=False)
    subject = models.CharField(
        max_length=100, default="No subject", blank=True)
    msg = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.msg)
