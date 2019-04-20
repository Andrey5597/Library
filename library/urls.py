from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-info'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('genres/', views.GenreListView.as_view(), name='genres'),
    path('mybooks/', views.BooksRentedByUserListView.as_view(), name='my-rented'),
    path('rentedbooks/', views.BooksRentedByUsersListView.as_view(), name='rented-books'),
    path('copy/create/', views.BookInstanceCreate.as_view(), name='copy_create'),
    path('copy/<int:pk>/update/', views.BookInstanceUpdate.as_view(), name='copy_update'),
]
