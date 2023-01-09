from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        default='/avatars/default.jpg', upload_to='avatars')
    summary = models.TextField(
        'Summary about user', default='New user on our platform!')
    location = models.TextField(
        'Place of residence', default='Location is not specified.')
    about = models.TextField(
        'About', default='Apparently, this user prefers to keep an air of mystery about them.')
    other_skills = models.CharField(max_length=30, null=True, blank=True)

    forgot_password_token = models.CharField(
        max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Account'


@receiver(post_save, sender=User)
def create_Profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)


class Follow(models.Model):
    following = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="follower")

    def __str__(self):
        return str(self.following.user.first_name)
