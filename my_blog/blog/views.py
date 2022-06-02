from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from .models import Article


# Create your views here.

class IndexView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'blog/index.html'


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog/detail.html'
