from django.shortcuts import render
from library.models import Book, BookInstance, BookDescription, BookSummary, BookComment, Shelf
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    """select count (book_title) from library_book;"""
    num_books = Book.objects.all().count()

    """select count (id) from library_BookInstance;"""
    num_instances = BookInstance.objects.all().count()

    """ select count (id) from library_BookInstance where status='a'; """
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    """select count (distinct author_name) from library_BookDescription;"""
    num_authors = BookDescription.objects.values('author_name').distinct().count()

    """select count (distinct genre) from library_BookDescription;"""
    num_genres = BookDescription.objects.values('genre').distinct().count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres': num_genres,
        'num_visits': num_visits,
    }

    return render(request, 'home.html', context=context)


class BookListView(generic.ListView):
    model = BookDescription
    context_object_name = 'book_list'

    """select * from library_BookDescription;"""
    queryset = BookDescription.objects.all()

    template_name = 'library/book_list.html'


class BookDetailView(generic.DetailView):
    model = BookDescription
    context_object_name = 'BookDescription'
    template_name = 'library/book_info.html'


class AuthorListView(generic.ListView):
    model = BookDescription
    context_object_name = 'author_list'

    """select distinct author_name from library_BookDescription;"""
    queryset = BookDescription.objects.values('author_name').distinct()

    template_name = 'library/author_list.html'


class BooksRentedByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'library/books_rented_by_user.html'
    context_object_name = 'rent_list'

    def get_queryset(self):
        return BookInstance.objects.filter(rent=self.request.user.id).filter(status__exact='o').order_by('due_back')