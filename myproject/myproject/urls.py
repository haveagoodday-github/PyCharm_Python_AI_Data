from django.urls import path
from myapp import views



urlpatterns = [
    path('hello/', views.my_view, name='hello'),
    path('search/', views.my_view, name='search_results'),
]
