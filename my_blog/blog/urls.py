from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('test_panel/', views.test_panel, name='test_panel'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_confirm/<uidb64>/<token>/',
         views.MyPasswordResetConfirmView.as_view(template_name='blog/reset_password_confirm.html'),
         name='reset_password_confirm'),
    path('reset_password_complete/', views.reset_password_complete, name='reset_password_complete')
]
