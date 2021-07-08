
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("network/profile/<int:user_id>", views.profile, name="profile"),
    path("network/following", views.following_view, name="following"),

    # API Routes
    path("network", views.compose, name="compose"),
    path("network/profile/follow/<int:user_id>", views.follow, name="follow"),
    path("network/profile/unfollow/<int:user_id>", views.unfollow, name="unfollow"),
    path("network/<str:posts>", views.post_view, name="posts"),
    path("network/like/<int:post_id>", views.like_view, name="like"),
    path("network/dislike/<int:post_id>", views.dislike_view, name="dislike"),
    path("network/edit/<int:post_id>", views.edit_view, name="edit"),
]
