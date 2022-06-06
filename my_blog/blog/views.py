from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView
from .models import Article
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

class IndexView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'blog/index.html'


class ArticleDetailView(DetailView):
    model = Article
    context_object_name = 'article'
    template_name = 'blog/detail.html'


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful")
            return redirect('blog:index')

        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render(request, 'blog/register.html', {'form': form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Welcome {username}")
                return redirect('blog:index')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})
