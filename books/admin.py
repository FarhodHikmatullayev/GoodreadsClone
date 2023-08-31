from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'isbn',)
    search_fields = ('title', 'isbn')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'email', 'bio')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'author')
    search_fields = ('author__first_name', 'book__title')


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'book', 'stars_given')
    search_fields = ('author__username',)
