from django.shortcuts import render
from library.models import Book, BookInstance, BookDescription
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q


def home(request):
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
    }
    return render(request, 'home.html', context=context)


def book_list(request):
    query = request.GET.get('q')
    """select * from library_BookDescription;"""
    queryset = BookDescription.objects.all()
    if query:
        queryset = queryset.filter(
            Q(book_title__icontains=query) |
            Q(author_name__icontains=query) |
            Q(genre__icontains=query)
        )

    context = {'book_list': queryset}
    return render(request, 'library/book_list.html', context=context)


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = BookDescription
    context_object_name = 'BookDescription'
    template_name = 'library/book_info.html'


class AuthorListView(generic.ListView):
    model = BookDescription
    context_object_name = 'author_list'

    """select distinct author_name from library_BookDescription;"""
    queryset = BookDescription.objects.values('author_name').distinct()

    template_name = 'library/author_list.html'


class GenreListView(generic.ListView):
    model = BookDescription
    context_object_name = 'genre_list'

    """select distinct genre from library_BookDescription;"""
    queryset = BookDescription.objects.values('genre').distinct()

    template_name = 'library/genre_list.html'


class BooksRentedByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'library/books_rented_by_user.html'
    context_object_name = 'rent_list'

    def get_queryset(self):
        ''' select * from library_BookInstance inner join auth_user on library_BookInstance.rent_id=auth_user.id
        where library_BookInstance.status='o' order by due_back '''
        return BookInstance.objects.filter(rent=self.request.user.id).filter(status__exact='o').order_by('due_back')


class BooksRentedByUsersListView(PermissionRequiredMixin, generic.ListView):
    permission_required = ('library.can_see_all_rented_books',)
    model = BookInstance
    template_name = 'library/books_rented_by_users.html'
    context_object_name = 'rent_list'

    def get_queryset(self):
        """select * from library_BookInstance where status='o' order by due_back;"""
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('books')


class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = ['due_back', 'status', 'rent']
    success_url = reverse_lazy('books')
