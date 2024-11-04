from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator


class Genre(models.Model):
    category_name = models.CharField(max_length=255)
    genre_image = models.ImageField(upload_to='image', blank=True, null=True, default='image/placeholder.jfif')

    class Meta:
        ordering = ['category_name']
        db_table = 'genre'



    def __str__(self):
        return self.category_name



class Book(models.Model):

    title = models.CharField(max_length=255, null=False, blank=True)
    author = models.CharField(max_length=255, null=False, blank=True)
    publisher = models.CharField(max_length=255, null=False, blank=True)
    publication_date = models.DateField(null=False, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    isbn = models.CharField(max_length=255, null=False, blank=True, unique=True)
    book_image = models.ImageField(upload_to='image', blank=True, null=True, default='image/placeholder.jfif')
    Description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['title']
        db_table = 'books'
    def __str__(self):
        return self.title



class Member(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=True)
    last_name = models.CharField(max_length=255, null=False, blank=True)
    email = models.EmailField(max_length=255, blank=False, unique=True, default='unknown address')
    address = models.CharField(max_length=255, null=False, blank=True)
    membership_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BookCopy(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    copy_number = models.IntegerField(validators=[MaxValueValidator(1000)], null=False, blank=False)
    status = models.CharField(max_length=20, choices=[
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
        ('issued', 'Issued'),
    ], default='available')

    class Meta:
        ordering = ['copy_number']
        db_table = 'book_copies'

    def __str__(self):
        return f"{self.book.title} - Copy {self.copy_number}"
    def is_available(self):
        return self.status == 'available'




class Borrow(models.Model):
    book_copy = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    borrow_date = models.DateTimeField(default=timezone.now, null=False)
    return_date = models.DateTimeField(default=timezone.now, null=False)

    def __str__(self):
        return f"{self.book_copy} borrowed by {self.member}"




