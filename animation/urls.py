from django.urls import path
from . import views

urlpatterns = [
    path('recommend/', views.my_recommend_view, name='recommend_page'),
]
