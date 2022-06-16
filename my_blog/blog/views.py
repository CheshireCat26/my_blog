from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, DetailView
from .models import Article
from .forms import NewUserForm, MyAuthenticationForm, MyPasswordResetForm, MySetPasswordForm


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

    def get_queryset(self):
        return Article.objects.filter(pub_date__lte=timezone.now())


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
        form = MyAuthenticationForm(request, data=request.POST)
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
    form = MyAuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out")
    return redirect('blog:index')


def test_panel(request):
    if not request.user.is_superuser:
        messages.error(request, 'Unauthorized access')
        return redirect('blog:index')

    if 'info_message' in request.POST.keys():
        messages.info(request, "Test info message")
    elif 'error_message' in request.POST.keys():
        messages.error(request, "Test error message")
    return render(request, 'blog/test_panel.html')


def reset_password(request):
    if request.method == "POST":
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            users = User.objects.filter(Q(email=email))
            if users.exists():
                for user in users:
                    subject = "Password Reset"
                    email_template = 'blog/password_reset_email.txt'
                    context = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'my_blog',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http'
                    }
                    email = render_to_string(email_template, context)
                    try:
                        send_mail(subject, email, 'example@gmail.com', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.info(request, "Mail sent")
                    return redirect('blog:index')

    form = MyPasswordResetForm()
    return render(request, 'blog/reset_password.html', {'form': form})


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = MySetPasswordForm
    success_url = reverse_lazy('blog:reset_password_complete')


def reset_password_complete(request):
    messages.info(request, "Password successfully changed")
    return redirect('blog:index')
