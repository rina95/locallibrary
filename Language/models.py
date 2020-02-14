from django.db import models

# Create your models here.
class Language(models.Model):
  name = models.CharField(max_length=200)

  class Meta:
    db_table = 'languages'

  def __str__(self):
    return self.name
