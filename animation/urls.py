from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.show_recommend_view, name='recommend_page'),
    path('bookmark/', views.show_bookmark_view, name='bookmark_page'),
]
