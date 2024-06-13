from django.urls import path
from . import views
from .views import search_news

urlpatterns = [
    path('', views.home, name='blog-home'),  # Убедитесь, что имя URL-шаблона соответствует этому
    path('contacts/', views.contacts, name='blog-contacts'),
    path('news/', views.news, name='blog-news'),
    path('news/<int:pk>/', views.NewsDetailView.as_view(), name='blog-novosti'),
    path('news/<int:pk>/update',views.NewsUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete',views.NewsDeleteView.as_view(), name='news_delete'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('search/', search_news, name='search_news'),
    path('profile/', views.profile, name='profile'),
    path('edit_pass/', views.ChangeFormView.as_view(), name='edit-pass'),
    path('create/',views.create, name='create'),
]