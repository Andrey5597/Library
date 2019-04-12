from django.shortcuts import render
from library.models import Book, BookInstance, BookDescription, BookSummary, BookComment, Shelf


def home(request):
    '''select count (book_title) from library_book;'''
    num_books = Book.objects.all().count()

    '''select count (id) from library_BookInstance;'''
    num_instances = BookInstance.objects.all().count()

    ''' select count (id) from library_BookInstance where status='a'; '''
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    '''select count (distinct author_name) from library_BookDescription;'''
    num_authors = BookDescription.objects.values('author_name').distinct().count()

    '''select count (distinct genre) from library_BookDescription;'''
    num_genres = BookDescription.objects.values('genre').distinct().count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
    }

    return render(request, 'home.html', context=context)



