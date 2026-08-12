from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.PostView.as_view()),
    path("posts/<slug:slug>/", views.PostDetailView.as_view()),
    path("books/", views.BookView.as_view()),
    path("books/<slug:slug>/", views.BookDetailView.as_view()),
]
