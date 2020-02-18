from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
  path('', views.index, name='index'),
  path('books/', views.BookListView.as_view(), name='books'),
  path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
  path('authors/', views.AuthorListView.as_view(), name='authors'),
  path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
  path('accounts/', include('django.contrib.auth.urls')),
  path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
  path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]
