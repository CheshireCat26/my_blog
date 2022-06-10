from datetime import timedelta

from django.db import models

# Create your models here.
from django.utils import timezone


class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField()
    last_edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_add_recently(self):
        return timezone.now() - timedelta(days=7) < self.pub_date <= timezone.now()
