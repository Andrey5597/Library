from django.shortcuts import render
from library.models import Book, BookInstance, BookDescription, BookSummary, BookComment, Shelf


def home(request):

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    #num_authors = BookDescription.objects.value('author_name').distinct().count()
    #num_genres = BookDescription.objects.value('genre').distinct().count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        #'num_authors': num_authors,
       # 'num_genres': num_genres,
    }

    return render(request, 'home.html', context=context)