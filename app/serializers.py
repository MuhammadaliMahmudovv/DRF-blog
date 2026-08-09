from rest_framework import serializers
from .models import CustomUser, Author, Category, Book, Post, Comment


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]

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
        user = CustomUser.objects.create_user(
            username=validated_data.get("username"),
            password=validated_data.get("password"),
        )
        return user


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
