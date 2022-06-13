from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import Article
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

class IndexView(ListView):
    model = Article
    context_object_name = 'article_list'
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        context = {'article_list': Article.objects.filter(pub_date__lte=timezone.now())}
        return context


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


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('blog:index')


def test_panel(request):
    if 'info_message' in request.POST.keys():
        messages.info(request, "Test info message")
    elif 'error_message' in request.POST.keys():
        messages.error(request, "Test error message")
    return render(request, 'blog/test_panel.html')
