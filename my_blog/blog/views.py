from django.http import HttpResponse
from django.views.generic import ListView
from .models import Article


# Create your views here.

class IndexView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'blog/index.html'


def detail(request, pk):
    return HttpResponse("There gonna be article's full text")
