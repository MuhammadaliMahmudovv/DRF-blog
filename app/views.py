from django.shortcuts import render
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from .models import Comment, Post, Book, Category, Author, CustomUser
from .serializers import (
    CommentSerializers,
    PostSerializer,
    BookSerializer,
    CategorySerializer,
    AuthorSerializer,
    CustomUserSerializer,
)


class PostView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class AuthorView(ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class CommentView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
