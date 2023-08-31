from rest_framework import serializers
from books.models import BookReview, Book
from users.models import User


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'description', 'isbn', 'cover_picture')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class BookReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BookReview
        fields = ('id', 'author', 'book', 'comment', 'stars_given', 'created_time', 'book_id', 'author_id')
