from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser): ...


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    authors = models.ManyToManyField(Author)
    categories = models.ManyToManyField(Category)
    cover = models.ImageField(upload_to="books/")
    publication_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    author_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="posts"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, blank=True, null=True, related_name="posts"
    )
    content = models.TextField()
    status = models.CharField(
        max_length=9, choices=STATUS_CHOICES, default=STATUS_CHOICES.DRAFT
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post} - {self.user}"
