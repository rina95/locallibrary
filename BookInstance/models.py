from django.db import models
import uuid
from Book.models import Book

# Create your models here.
class BookInstance(models.Model):
  LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
  )

  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  imprint = models.CharField(max_length=200)
  due_back = models.DateField(null=True, blank=True)
  status = models.CharField(
            max_length=1,
            choices=LOAN_STATUS,
            blank=True,
            default='m',
            help_text='Book availability',
          )

  book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

  class Meta:
    ordering = ['due_back']

  def __str__(self):
    return f'{self.id} ({self.book.title})'
  
