from django.db import models
from django.urls import reverse
from Genre.models import Genre
from Author.models import Author
from Language.models import Language

# Create your models here.
class Book(models.Model):
  title = models.CharField(max_length=200)
  summary =models.TextField(max_length=1000, help_text="Enter description of the book")
  isbn = models.CharField("ISBN", max_length=13, 
    help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

  genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
  author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
  language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

  class Meta:
    db_table = "books"

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])

  def display_genre(self):
    return ', '.join(genre.name for genre in self.genre.all()[:3])

  display_genre.short_description = 'Genre'
