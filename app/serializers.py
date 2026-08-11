from rest_framework import serializers
from .models import CustomUser, Author, Category, Book, Post, Comment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        has_digits = any(char.isdigit() for char in value)
        has_letters = any(char.isalpha() for char in value)
        if not has_digits or not has_letters:
            raise serializers.ValidationError(
                "Password must contain digits and letters"
            )
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters"
            )
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data.get("username"),
            password=validated_data.get("password"),
        )


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategoryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title", "slug"]


class AuthorBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "last_name", "slug"]


class PostBookSerializer(serializers.ModelSerializer):
    authors = AuthorBookSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "cover", "authors"]


class PostAuthorUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    book = PostBookSerializer(read_only=True)
    author_user = PostAuthorUserSerializer(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "slug",
            "content",
            "book",
            "author_user",
            "rating",
            "created_at",
            "comments_count",
        ]


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorBookSerializer(many=True, read_only=True)
    categories = CategoryBookSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "slug",
            "authors",
            "categories",
            "cover",
            "publication_year",
            "isbn",
        ]


class BookPostSerializer(serializers.ModelSerializer):
    author_user = PostAuthorUserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "author_user", "rating", "created_at"]


class BookDetailSerializer(serializers.ModelSerializer):
    authors = AuthorBookSerializer(many=True, read_only=True)
    categories = CategoryBookSerializer(many=True, read_only=True)
    posts = BookPostSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "slug",
            "authors",
            "categories",
            "cover",
            "publication_year",
            "isbn",
            "posts",
        ]
