from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:pk>/detail/", views.detail, name="detail"),
    path("<int:pk>/edit_profile/", views.edit_profile, name="edit_profile"),
    path("<int:pk>/password/", views.change_password, name="change_password"),
    path("<int:pk>/follow/", views.follow, name="follow"),
    path("<int:pk>/message/", views.message, name="message"),
    path("login/github", views.social_signup_request, name="social"),
    path("login/github/callback", views.social_signup_callback),
    path("<int:pk>/send/", views.send, name="send"),
]