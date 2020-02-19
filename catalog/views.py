import datetime

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.forms import RenewBookForm
from catalog.forms import RenewBookModelForm

from django.shortcuts import render
from django.views import generic
from catalog.models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
  """Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name ='catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 10
  
  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksListView(generic.ListView):
  """Generic class-based view listing books on loan to current user."""
  model = BookInstance
  template_name ='catalog/bookinstance_list_loaned.html'
  paginate_by = 10
  
  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
  book_instance = get_object_or_404(BookInstance, pk=pk)

  # If this is a POST request then process the Form data
  if request.method == 'POST':

    # Create a form instance and populate it with data from the request (binding):
    form = RenewBookModelForm(request.POST)

    # Check if the form is valid:
    if form.is_valid():
      # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
      book_instance.due_back = form.cleaned_data['due_back']
      book_instance.save()

      # redirect to a new URL:
      return HttpResponseRedirect(reverse('all-borrowed') )

  # If this is a GET (or any other method) create the default form.
  else:
    proposed_due_back = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookModelForm(initial={'due_back': proposed_due_back})

  context = {
    'form': form,
    'book_instance': book_instance,
  }

  return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(LoginRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(LoginRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
