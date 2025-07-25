# shortener/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The homepage route
    path('', views.home_view, name='home'),
    # The API endpoint for creating a link
    path('create/', views.create_short_url, name='create'),
    # The dynamic redirect route that captures the short code
    path('<str:short_code>/', views.redirect_view, name='redirect'),
]