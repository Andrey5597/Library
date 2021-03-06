from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date


class Book(models.Model):
    shelf_id = models.ForeignKey('Shelf', on_delete=models.SET_NULL, null=True)
    book_title = models.CharField(max_length=50, verbose_name='Title', default='Book')

    def __str__(self):
        return self.book_title


class Shelf(models.Model):
    shelf_name = models.CharField(max_length=2, null=True, verbose_name='Shelf number')

    def __str__(self):
        return self.shelf_name

    class Meta:
        verbose_name_plural = 'Shelves'


class BookDescription(models.Model):
    book = models.OneToOneField('Book', on_delete=models.CASCADE, null=True)
    book_title = models.CharField(max_length=50, verbose_name='Title')
    isbn = models.CharField(max_length=13)
    author_name = models.CharField(max_length=20, verbose_name='Author name')
    published = models.DateField(verbose_name='Date of publish')
    number_of_pages = models.IntegerField(verbose_name='Number of pages')
    genre = models.CharField(max_length=20, verbose_name='Genre')
    book_summary = models.OneToOneField('BookSummary', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.book_title

    def get_absolute_url(self):
        return reverse('book-info', args=[str(self.pk)])


class BookSummary(models.Model):
    book_summary = models.TextField(max_length=1000, verbose_name='Book summary')
    book = models.OneToOneField('Book', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'summary of {self.book}'


class BookInstance(models.Model):
    book = models.ForeignKey('BookDescription', on_delete=models.CASCADE, null=True)
    due_back = models.DateField(null=True, blank=True)
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True)
    rent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_see_all_rented_books", "List of rented books"),)

    def __str__(self):
        return self.book.book_title

    def get_absolute_url(self):
        return reverse('copy_update', args=[str(self.pk)])


