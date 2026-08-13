from django.db.models import Count, Prefetch
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from .models import Comment, Post, Book, Category, Author, CustomUser
from .serializers import (
    PostSerializer,
    BookSerializer,
    BookDetailSerializer,
    AuthorSerializer,
    CustomUserSerializer,
    PostDetailSerializer,
    AuthorDetailSerializer,
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


class PostDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = (
        Post.objects.filter(status=Post.STATUS_CHOICES.PUBLISHED)
        .select_related("book", "author_user")
        .prefetch_related(
            "book__authors",
            "book__categories",
            "comments__user",
        )
    )
    serializer_class = PostDetailSerializer


class BookView(ListAPIView):
    queryset = Book.objects.prefetch_related("authors", "categories").all()
    serializer_class = BookSerializer


class BookDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Book.objects.prefetch_related(
        "authors",
        "categories",
        Prefetch(
            "posts",
            queryset=Post.objects.filter(
                status=Post.STATUS_CHOICES.PUBLISHED
            ).select_related("author_user"),
        ),
    ).all()
    serializer_class = BookDetailSerializer


class AuthorView(ListAPIView):
    queryset = Author.objects.all().annotate(books_count=Count("book"))
    serializer_class = AuthorSerializer


class AuthorDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Author.objects.prefetch_related("book_set")
    serializer_class = AuthorDetailSerializer
