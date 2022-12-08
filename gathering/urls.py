from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "gathering"

urlpatterns = [
    path("list/", views.gathering_list, name="gathering-list"),
    path("create/", views.gathering_create, name="gathering-create"),
    path("<int:gathering_id>/", views.gathering_detail, name="gathering-detail"),
    path("edit/<int:gathering_id>/", views.gathering_edit, name="gathering-edit"),
    path("delete/<int:gathering_id>/", views.gathering_delete, name="gathering-delete"),
    path("end/<int:gathering_id>/", views.end_gathering, name="end_gathering"),
    path("edit/<int:gathering_id>/choice/add/", views.add_choice, name="add_choice"),
    path("edit/choice/<int:choice_id>/", views.choice_edit, name="choice_edit"),
    path("delete/choice/<int:choice_id>/", views.choice_delete, name="choice_delete"),
    path("<int:gathering_id>/vote/", views.gathering_vote, name="vote"),
    # 댓글
    path("<int:gathering_id>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:gathering_id>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path(
        "<int:gathering_id>/comments/<int:comment_pk>/update/",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:gathering_id>/comments/<int:comment_pk>/update/complete/",
        views.comment_update_complete,
        name="comment_update_complete",
    ),
    path("<int:gathering_id>/like/", views.like, name="like"),
    path("meeting_offline/", views.meeting_offline, name="meeting_offline"),
    path("search/", views.search, name="search"),
]
