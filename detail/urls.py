from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.show_detail_view, name='detail'),
]