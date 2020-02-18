from django.db import models
import uuid
from Book.models import Book
from django.contrib.auth.models import User
from datetime import date

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
  borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

  class Meta:
    ordering = ['due_back']
    permissions = (("can_mark_returned", "Set book as returned"),) 

  def __str__(self):
    return f'{self.id} ({self.book.title})'
  
  @property
  def is_overdue(self):
    if self.due_back and date.today() > self.due_back:
      return True
    return False
