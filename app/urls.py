from django.urls import path
from . import views

urlpatterns = [
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
