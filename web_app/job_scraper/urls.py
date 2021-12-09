from django.urls import path
from . import views

app_name = 'job_scraper'
urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('search', views.SearchView.as_view(), name='search')
]