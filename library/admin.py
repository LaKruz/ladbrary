from django.contrib import admin

from .models import Author, Book, Comment


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    ...


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    ...


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    ...
