from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/<int:id>', views.show_recommend_view, name='recommend_page'),
]
