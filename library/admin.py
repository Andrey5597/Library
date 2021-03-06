from django.contrib import admin
from .models import Book, Shelf, BookDescription, BookSummary, BookInstance


class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'shelf_id')
    list_display_links = ('book_title',)
    search_fields = ('book_title',)


class ShelfAdmin(admin.ModelAdmin):
    list_display = ['shelf_name']


class BookDescriptionAdmin(admin.ModelAdmin):
    list_display = ('book_title', 'isbn', 'author_name',
                    'genre', 'published', 'number_of_pages')
    list_display_links = ('book_title',)
    search_fields = ('author_name', 'genre', 'book_title')


class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'rent', 'due_back')
    list_display_links = ('book',)
    list_filter = ('status', 'due_back')
    search_fields = ('book',)


admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Shelf, ShelfAdmin)
admin.site.register(BookSummary)
admin.site.register(BookDescription, BookDescriptionAdmin)
