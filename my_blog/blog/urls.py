from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout')
]
