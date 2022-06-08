from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('main/', views.main_view, name='mainpage'),
    path('recommend/', views.show_recommend_view, name='recommend_page'),
    path('bookmark/', views.show_bookmark_view, name='bookmark_page'),
    path('search/', views.search_view, name='search_animation'),
    path('genre/<int:id>', views.genre_view, name='genrepage'),

]
