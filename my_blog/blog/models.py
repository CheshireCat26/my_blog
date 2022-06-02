from django.db import models


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField()
    last_edit_date = models.DateTimeField(auto_now=True)
