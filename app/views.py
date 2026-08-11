from django.db.models import Count
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from .models import Comment, Post, Book, Category, Author, CustomUser
from .serializers import (
    PostSerializer,
    BookSerializer,
    BookDetailSerializer,
    AuthorSerializer,
    CustomUserSerializer,
)


class PostView(ListAPIView):
    queryset = (
        Post.objects.filter(status=Post.STATUS_CHOICES.PUBLISHED)
        .select_related("book", "author_user")
        .prefetch_related("book__authors")
        .annotate(comments_count=Count("comments"))
        .order_by("-created_at")
    )
    serializer_class = PostSerializer


class BookView(ListAPIView):
    queryset = Book.objects.prefetch_related("authors", "categories").all()
    serializer_class = BookSerializer


class BookDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Book.objects.prefetch_related(
        "authors",
        "categories",
        "posts__author_user",
    ).all()
    serializer_class = BookDetailSerializer


class AuthorView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
