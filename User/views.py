from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from Home.models import Project, Skill
from django.contrib.auth.decorators import login_required
import uuid
from django.core.mail import send_mail
from django.conf import settings
from User.models import Follow
# Create your views here.


def login_page(request):

    if request.method == "POST":
        email = request.POST.get("email")
        email = str(email).lower()
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("Index")
        else:
            messages.warning(request, "Incorrect Username Or Password")

    return render(request, "login.html")


def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        username = request.POST.get("username")
        username = str(username).lower()
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm-password")
        if User.objects.filter(username=username):

            messages.warning(request, "Username is Already Taken ")
            return redirect("Signup")
        elif password != confirm_password:
            messages.warning(
                request, "The Two Password Field Is not matching ")
            return redirect("Signup")
        user = User.objects.create(
            first_name=name, username=username, email=email)
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)

            return redirect("Account_edit")

    return render(request, "signup.html")


@login_required(login_url="Login")
def account_edit(request):
    user = Profile.objects.get(user=request.user)
    if request.method == "POST":
        summary = request.POST.get("summary")
        location = request.POST.get("location")
        about = request.POST.get("about")
        skills = request.POST.get("skills")
        avatar = request.FILES.get("avatar")

        user.summary = summary
        user.about = about
        user.location = location
        user.skills = skills
        if avatar != None:
            user.avatar = avatar
        user.save()
        return redirect("My_account")
    context = {"user": user}
    return render(request, "account-edit-form.html", context)


def signout(request):
    logout(request)
    return redirect("Login")


def User_Profile(request, pk):
    profile = Profile.objects.get(user__username=pk)
    projects = Project.objects.filter(profile=profile)
    skills = Skill.objects.filter(profile=profile)
    if request.user.is_authenticated:
        user = request.user
        user_profile = Profile.objects.filter(user=user).first()
        print(" Look at this ", user_profile)
        if Follow.objects.filter(following=profile, follower=user_profile).first():
            text = "Unfollow"
        else:
            text = "Follow"
        context = {"profile": profile, 'projects': projects,
                   'skills': skills, "text": text}
        return render(request, 'profile.html', context)
    else:
        context = {"profile": profile, 'projects': projects,
                   'skills': skills}
        return render(request, 'profile.html', context)


def forgot_password(request):
    try:
        if request.method == "POST":
            email = request.POST.get("email")
            if not User.objects.filter(email=email).first():
                messages.warning(request, "User Not Found")
                return redirect("Forgot_password")
            user = User.objects.get(email=email)
            profile = Profile.objects.get(user=user)
            token = str(uuid.uuid4())
            send_mail("Password Reset Verification Mail", f"Please Click On The Link To Verify  http://127.0.0.1:8000/Account/Change_passsword/{token}", settings.EMAIL_HOST_USER,
                      [email], fail_silently=False)
            profile.forgot_password_token = token
            profile.save()

            return redirect("Password_sent")
        return render(request, 'forgetpassword.html')
    except Exception as e:
        print(e)
        messages.warning(request, "An Error Happen Please Try Again")
        return redirect("Forgot_password")


def change_password(request, pk):
    if Profile.objects.filter(forgot_password_token=pk).first():
        profile = Profile.objects.get(forgot_password_token=pk)
        user = profile.user
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get("password2")
            if password1 != password2:
                messages.warning(
                    request, "The Two Password Field is not matching")
                return redirect("Change_password", pk=pk)
            user.set_password(password1)
            user.save()
            messages.warning(request, "Password has been reset")
            return redirect("Login")
    else:
        messages.warning(request, "Enter Valid Token Please Re-try")
        return redirect("Forgot_password")
    print(pk)
    return render(request, 'reset.html')


def password_sent(request):
    return render(request, "reset_password_sent.html")


@login_required(login_url="Login")
def follow(request, pk):
    try:
        user = request.user
        follower_profile = Profile.objects.get(user=user)
        following_profile = Profile.objects.get(id=pk)

        p = Follow.objects.filter(
            following=following_profile, follower=follower_profile).first()

        if Follow.objects.filter(following=following_profile, follower=follower_profile).first():
            follow_obj = Follow.objects.get(following=following_profile,
                                            follower=follower_profile)
            follow_obj.delete()
            return redirect("Profile", pk=following_profile.user.username)
        else:
            Follow.objects.create(following=following_profile,
                                  follower=follower_profile)

        return redirect("Profile", pk=following_profile.user.username)
    except Exception as e:
        print(e)
        messages.warning("An Error Occour Please Try Again")
        return redirect("Profile", pk=following_profile.user.username)
