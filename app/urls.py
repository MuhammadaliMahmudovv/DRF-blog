from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views

urlpatterns = [
    path("auth/register/", views.UserRegisterView.as_view(), name="auth-register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="auth-login"),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="auth-token-refresh",
    ),
    path("auth/logout/", TokenBlacklistView.as_view(), name="auth-logout"),
    path("posts/", views.PostView.as_view()),
    path("posts/create/", views.PostCreateView.as_view()),
    path("posts/<slug:slug>/", views.PostDetailView.as_view()),
    path("posts/<slug:slug>/update/", views.PostUpdateView.as_view()),
    path("posts/<slug:slug>/destroy/", views.PostDestroyView.as_view()),
    path("books/", views.BookView.as_view()),
    path("books/create/", views.BookCreateView.as_view()),
    path("books/<slug:slug>/", views.BookDetailView.as_view()),
    path("authors/", views.AuthorView.as_view()),
    path("authors/<slug:slug>/", views.AuthorDetailView.as_view()),
]
