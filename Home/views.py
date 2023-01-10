from django.shortcuts import render, redirect
from User.models import Profile
from Home.models import Project, Comment, Skill, New_msg, Like
from .helper import Paginator_function
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
# Create your views here.


def index(request):
    profiles = Profile.objects.all()
    page = request.GET.get("page")
    profiles = Paginator_function(profiles, 3, page)
    if request.method == "POST":
        search = request.POST.get("search")
        if cache.get("search"):
            profiles = cache.get("search")
            print("From Cache")
        else:
            profiles = Profile.objects.filter(
                user__first_name__istartswith=search)
            cache.set("search", profiles, timeout=100)
            print("From Database")
    context = {"profiles": profiles}
    return render(request, 'index.html', context)


@login_required(login_url="Login")
def add_project(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        link = request.POST.get("link")
        image = request.FILES.get("image")

        user = request.user
        profile = Profile.objects.get(user=user)

        pro = Project.objects.create(profile=profile, name=title,
                                     about=description, source_code=link, image=image)
        return redirect("My_account")
    return render(request, "project-add-edit-form.html")


@login_required(login_url="Login")
def my_account(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    all_projects = Project.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile)

    context = {"profile": profile,
               "all_projects": all_projects, 'skills': skills}
    return render(request, "account.html", context)


def projects(request):
    all_projects = Project.objects.all()[::-1]
    page = request.GET.get("page")
    all_projects = Paginator_function(all_projects, 2, page)
    if request.method == "POST":
        search = request.POST.get("search")
        all_projects = Project.objects.filter(name__istartswith=search)

    context = {"projects": all_projects}
    return render(request, "projects.html", context)


def single_project(request, pk):
    project = Project.objects.get(id=pk)
    comments = Comment.objects.filter(project=project)[::-1]

    text = False
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)
        if Like.objects.filter(project=project, profile=profile):
            text = True
        else:
            text = False
    if request.method == "POST":
        user = request.user
        profile = Profile.objects.get(user=user)
        msg = request.POST.get("message")
        Comment.objects.create(profile=profile, project=project, msg=msg)
        return redirect("Single_project", pk=project.id)
    context = {"project": project, 'comments': comments, 'text': text}
    return render(request, "single-project.html", context)


@login_required(login_url="Login")
def add_skills(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == "POST":
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        Skill.objects.create(profile=profile, skill_name=name, skill_bio=bio)
        return redirect("My_account")
    return render(request, 'skill-add-edit-form.html')


@login_required(login_url="Login")
def delete_skill(request, pk):
    skill = Skill.objects.get(id=pk)

    if request.method == "POST":

        skill.delete()
        return redirect("My_account")
    context = {'skill': skill}
    return render(request, 'delete.html', context)


@login_required(login_url="Login")
def inbox(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    new_messages = New_msg.objects.filter(receiver=profile)[::-1]
    unread = New_msg.objects.filter(receiver=profile, is_read=False).count()

    context = {'messages': new_messages, 'unread': unread}
    return render(request, 'inbox.html', context)


@login_required(login_url="Login")
def view_msg(request, pk):
    message = New_msg.objects.get(id=pk)
    message.is_read = True
    message.save()
    context = {'message': message}
    return render(request, 'message.html', context)


@login_required(login_url="Login")
def send_msg(request, pk):
    receiver_profile = Profile.objects.get(id=pk)
    sender_profile = Profile.objects.get(user=request.user)
    print(sender_profile, receiver_profile)
    if request.method == "POST":
        subject = request.POST.get("subject")
        msg = request.POST.get("text")
        New_msg.objects.create(
            sender=sender_profile, receiver=receiver_profile, subject=subject, msg=msg)
        messages.success(request, "Message Has Been Sent To the User")
        return redirect("Profile", pk=receiver_profile.user.username)
    return render(request, "send-message.html")


@login_required(login_url="Login")
def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        if request.user == project.profile.user:
            project.delete()
            messages.warning(request, "Project has been Deleted")
        return redirect("My_account")
    context = {"project": project}
    return render(request, 'delete.html', context)


def edit_skill(request, pk):
    skill = Skill.objects.get(id=pk)
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == "POST":
        name = request.POST.get("name")
        bio = request.POST.get("bio")
        print(name)

        skill.skill_name = name
        skill.skill_bio = bio
        skill.save()
        return redirect("My_account")
    context = {"skill": skill}
    return render(request, 'skill-add-edit-form.html', context)


def edit_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        name = request.POST.get("title")
        about = request.POST.get("description")
        source_code = request.POST.get("link")
        image = request.FILES.get("image")
        project.name = name
        project.about = about
        project.source_code = source_code
        if image == None:
            project.save()
        else:
            project.image = image
            project.save()
        return redirect("My_account")
    context = {'project': project}
    return render(request, 'project-add-edit-form.html', context)


@login_required(login_url="Login")
def like(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user
    profile = Profile.objects.get(user=user)
    if Like.objects.filter(project=project, profile=profile).first():
        like = Like.objects.get(project=project, profile=profile)
        like.delete()
        project.no_of_likes -= 1
        project.save()
    else:
        like = Like.objects.create(project=project, profile=profile)
        like.save()
        project.no_of_likes += 1
        project.save()
    return redirect("Single_project", pk=pk)
