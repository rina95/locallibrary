from django.contrib import admin
from Genre.models import Genre
from Author.models import Author
from Language.models import Language
from Book.models import Book
from BookInstance.models import BookInstance

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
  pass

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  pass
