from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.sign_up_view, name='sign_up'),
    path('select_genre/', views.select_genre_view, name='select_genre'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name='logout'),
]
