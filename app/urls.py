from django.urls import path
from . import views

urlpatterns = [
    path("authors/", views.AuthorView.as_view()),
    path("categories/", views.CategoryView.as_view()),
    path("books/", views.BookView.as_view()),
    path("posts/", views.PostView.as_view()),
    path("comments/", views.CommentView.as_view()),
]
