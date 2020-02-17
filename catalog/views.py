from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
  """View function for home page of site."""

  # Generate counts of some of the main objects
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()
  num_genres = Genre.objects.all().count()
  
  # Available books (status = 'a')
  num_instances_available = BookInstance.objects.filter(status__exact='a').count()
  
  # The 'all()' is implied by default.    
  num_authors = Author.objects.count()
  
  context = {
    'num_genres': num_genres,
    'num_books': num_books,
    'num_instances': num_instances,
    'num_instances_available': num_instances_available,
    'num_authors': num_authors,
  }

  # Render the HTML template index.html with the data in the context variable
  return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
  model = Book
  context_object_name = 'my_book_list'   # your own name for the list as a template variable
  paginate_by = 10

  def get_queryset(self):
    return Book.objects.all() # Get 5 books containing the title war
  # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location

class BookDetailView(generic.DetailView):
  model = Book

  def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    
    return render(request, 'Book/book_detail.html', context={'book': book})

class AuthorListView(generic.ListView):
  model = Author
  context_object_name = 'my_author_list'   # your own name for the list as a template variable
  paginate_by = 10

  def get_queryset(self):
    return Author.objects.all() # Get 5 Authors containing the title war
  # template_name = 'Authors/my_arbitrary_template_name_list.html'  # Specify your own template name/location

class AuthorDetailView(generic.DetailView):
  model = Author

  def author_detail_view(request, primary_key):
    try:
        author = Author.objects.get(pk=primary_key)
    except Author.DoesNotExist:
        raise Http404('author does not exist')
    
    return render(request, 'Author/author_detail.html', context={'author': author})
