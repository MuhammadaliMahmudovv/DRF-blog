import uuid
from django.db.models import Count, Prefetch
from django.utils.text import slugify
from .permissions import IsPostAuthor
from rest_framework.permissions import IsAuthenticated, AllowAny
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
    PostCreateSerializer,
    BookDetailSerializer,
    AuthorSerializer,
    CustomUserSerializer,
    PostDetailSerializer,
    AuthorDetailSerializer,
    UserRegistrationSerializer,
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


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        title = serializer.validated_data.get("title")
        unique_slug = f"{slugify(title)}-{uuid.uuid4().hex[:6]}"
        serializer.save(author_user=self.request.user, slug=unique_slug)


class PostUpdateView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    lookup_field = "slug"
    permission_classes = [IsAuthenticated, IsPostAuthor]


class PostDestroyView(DestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = "slug"
    permission_classes = [IsAuthenticated, IsPostAuthor]


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


class BookCreateView(CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class AuthorView(ListAPIView):
    queryset = Author.objects.all().annotate(books_count=Count("book"))
    serializer_class = AuthorSerializer


class AuthorDetailView(RetrieveAPIView):
    lookup_field = "slug"
    queryset = Author.objects.prefetch_related("book_set")
    serializer_class = AuthorDetailSerializer


class UserRegisterView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
