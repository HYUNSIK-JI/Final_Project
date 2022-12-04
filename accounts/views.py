from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth import get_user_model, login as my_login, logout as my_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import *
from articles.models import Comment as Comment1, Articles
from free.models import Comment as Comment2, Free
from django.db.models import Q
from .models import User
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from .forms import CustomUserChangeForm, CreateUser, SNSUserSignupForm
import os, requests

# Create your views here.

# 임시메인
def index(request):
    context = {
        "datas": get_user_model().objects.all(),
        "user": request.user,
    }
    return render(request, "accounts/index.html", context)


# 회원가입
def signup(request):
    # print(request)
    # if request.method == "POST":
    #     form = CreateUser(request.POST, request.FILES)
    #     print(1)
    #     if form.is_valid():
    #         user = form.save()
    #         my_login(request, user)
    #         print(2)
    #         return redirect("accounts:index")
    #     else:
    #         messages.warning(request, "이미 존재하는 ID입니다.")

    # else:
    #     form = CreateUser()
    #     print(3)
    # context = {
    #     "form": form,
    # }
    # print(form.errors)

    # return render(request, "accounts/signup.html", context)
    if request.method == "POST":
        signup_form = CreateUser(request.POST, request.FILES)
        sns_signup_form = SNSUserSignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            print(user)
            # 소셜 서비스 구분
            user.social_id = (
                request.POST["social_id"] if "social_id" in request.POST else None
            )
            user.service_name = (
                request.POST["service_name"] if "service_name" in request.POST else None
            )
            user.is_social_account = (
                True if "is_social_account" in request.POST else False
            )
            user.social_profile_picture = (
                request.POST["social_profile_picture"]
                if "social_profile_picture" in request.POST
                else None
            )
            # 유저 토큰
            user.token = request.POST["token"] if "token" in request.POST else None
            user.save()
            my_login(request, user)
            if user.is_social_account:
                return redirect("accounts:index")
            else:
                return redirect("accounts:index")
    else:
        signup_form = CreateUser()
    context = {
        "form": signup_form,
    }
    return render(request, "accounts/signup.html", context)


# 회원탈퇴
def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        user.delete()
    return redirect("accounts:index")


# 로그인
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(1)
        if form.is_valid():
            my_login(request, form.get_user())
            return redirect(request.GET.get("next") or "accounts:index")
        else:
            form = AuthenticationForm()
            messages.warning(request, "ID가 존재하지 않거나 암호가 일치하지 않습니다.")
            context = {"form": form}
            return render(request, "accounts/login.html", context)
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


# 로그아웃
@login_required
def logout(request):
    my_logout(request)
    return redirect("accounts:index")


# 디테일
@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    comments1 = Comment1.objects.filter(user_id=pk)  # 질문게시판 댓글
    articles = Articles.objects.filter(user_id=pk)  # 질문게시판 글

    comments2 = Comment2.objects.filter(user_id=pk)  # 자유게시판 댓글
    frees = Free.objects.filter(user_id=pk)  # 자유게시판 글
    if request.user.is_authenticated:
        new_message = Notification.objects.filter(
            Q(user_id=user.pk) & Q(check=False)
        )  # 알람있는지없는지 파악
        message_count = len(new_message)
        context = {
            "count": message_count,
            "user": user,
            "followers": user.followers.all(),
            "followings": user.followings.all(),
            "comments1": comments1,
            "articles": articles,
            "comments2": comments2,
            "frees": frees,
        }
    else:
        context = {
            "user": user,
        }
    return render(request, "accounts/detail.html", context)


# 프로필 수정
@login_required
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(
                request.POST, request.FILES, instance=request.user
            )
            print(2)
            if form.is_valid():
                print(1)
                form.save()
                return redirect("accounts:detail", user.pk)
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            "form": form,
        }
        return render(request, "accounts/edit_profile.html", context)
    else:
        return redirect("accounts:index")


@login_required
def change_password(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect("accounts:edit_profile", user.pk)
            else:
                messages.error(request, "Please correct the error below.")
        else:
            form = PasswordChangeForm(request.user)

        context = {
            "form": form,
        }

        return render(request, "accounts/change_password.html", context)
    else:
        return render(request, "accounts/index.html")


def message(request, pk):
    noti = Notification.objects.get(pk=pk)
    noti.check = True
    noti.save()
    id = noti.nid
    if noti.category == "자유":
        if Free.objects.filter(id=id).exists():
            return redirect("free:detail", id)
        else:
            return redirect("free:fail")
    elif noti.category == "질문":
        if Articles.objects.filter(id=id).exists():
            return redirect("articles:detail", id)
        else:
            return redirect("articles:fail")
    elif noti.category == "모임":
        print("모임", 3)
        return redirect("gathering:detail", id)


@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user != user:
        if request.user not in user.followers.all():
            user.followers.add(request.user)
            is_following = True
        else:
            user.followers.remove(request.user)
            is_following = False

    data = {
        "isFollowing": is_following,
        "followers": user.followers.all().count(),
        "followings": user.followings.all().count(),
    }

    return JsonResponse(data)


def social_signup_request(request):
    if "github" in request.path:
        service_name = "github"
    services = {
        "github": {
            "base_url": "https://github.com/login/oauth/authorize",
            "client_id": "addba30b16251115a79c",
            "redirect_uri": "http://127.0.0.1:8000/accounts/login/github/callback",
            "scope": "read:user",
        },
    }
    for k, v in services[service_name].items():
        if k == "base_url":
            res = f"{v}?"
        else:
            res += f"{k}={v}&"
    return redirect(res)


def social_signup_callback(request):
    if "github" in request.path:
        service_name = "github"
    services = {
        "github": {
            "data": {
                "redirect_uri": "http://127.0.0.1:8000/accounts/login/github/callback",
                "client_id": "addba30b16251115a79c",
                "client_secret": "60e071cf669b351b3cad4bffe929bd79eaf5476b",
                "code": request.GET.get("code"),
            },
            "api": "https://github.com/login/oauth/access_token",
            "user_api": "https://api.github.com/user",
        },
    }
    if service_name == "github":
        headers = {
            "accept": "application/json",
        }
        token = requests.post(
            services[service_name]["api"],
            data=services[service_name]["data"],
            headers=headers,
        ).json()
    # ================================== 액세스 토큰 발급 ==================================
    access_token = token["access_token"]
    print(access_token, 555)
    # ================================== 액세스 토큰 발급 ==================================
    payload = {
        "github": {"Authorization": f"token {access_token}"},
    }
    if service_name == "github":
        headers = payload[service_name]
        u_info = requests.get(
            services[service_name]["user_api"], headers=headers
        ).json()
    print(
        u_info, 111111111111111111111111111111111111111111111111111111111111111111111111
    )
    if service_name == "github":
        login_data = {
            "github": {
                "social_id": u_info["id"],
                "username": u_info["login"],
                "social_profile_picture": u_info["avatar_url"],
                "nickname": u_info["login"],
                "email": u_info["email"],
                ### 깃허브에서만 가져오는 항목 ###
                "git_username": u_info["login"],
                ### 깃허브에서만 가져오는 항목 ###
            },
        }
    user_info = login_data[service_name]
    print(
        user_info,
        222222222222222222222222222222222222222222222222222222222222222222222222,
    )
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        my_login(request, user)
        return redirect(request.GET.get("next") or "accounts:index")
    else:
        social_data = {
            # 소셜 서비스 구분
            "social_profile_picture": user_info["social_profile_picture"],
            "social_id": str(user_info["social_id"]),
            "service_name": service_name,
            "is_social_account": True,
            # 유저 토큰 가져오기
            "token": access_token,
        }
        data = {
            # 일반 정보
            "username": user_info["git_username"],
            "nickname": user_info["nickname"],
            "email": user_info["email"],
            # 깃허브에서만 가져오는 항목
            "git_username": (u_info["login"] if service_name == "github" else None),
        }
        signup_form = CreateUser(initial=data)
        sns_signup_form = SNSUserSignupForm(initial=social_data)
        context = {
            "form": signup_form,
            "sns_signup_form": sns_signup_form,
        }
    return render(request, "accounts/signup.html", context)
