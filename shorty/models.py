from django.db import models

# Create your models here.
class URL(models.Model):
    
    shortURL = models.CharField(max_length=50, primary_key=True)
    longURL = models.CharField(max_length=50)
