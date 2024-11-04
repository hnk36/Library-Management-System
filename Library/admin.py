from django.contrib import admin
from . import models
@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'genre_image']
    list_editable = ['category_name', 'genre_image']
@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'publisher', 'publication_date', 'genre', 'isbn', 'book_image']
    list_editable = ['title', 'author', 'publisher', 'publication_date', 'genre', 'isbn', 'book_image']
    search_fields = ['title', 'author', 'isbn']
    list_filter = ['genre', 'author']
    fields = ['title', 'author', 'publisher', 'publication_date', 'genre', 'isbn']



@admin.register(models.BookCopy)
class BookCopyAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'copy_number', 'status']
    list_edit = ['book', 'copy_number', 'status']
    search_fields = ['book__title', 'book__author']

@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'membership_date']
    list_editable = ['first_name', 'last_name', 'email', 'address', 'membership_date']
    search_fields = ['email']
    list_filter = ['membership_date', 'first_name', 'last_name']
@admin.register(models.Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['id', 'book_copy', 'member', 'borrow_date']

