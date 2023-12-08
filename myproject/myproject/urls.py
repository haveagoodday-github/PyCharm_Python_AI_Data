from django.urls import path
from myapp import views



urlpatterns = [
    # path('hello/', views.my_view, name='hello'),
    path('search/', views.my_view, name='search_results'),
    path('search_results_for_tags/', views.search_by_bags, name='search_results_for_tags'),
    path('search_results_for_author/', views.search_by_author, name='search_results_for_author'),
]
