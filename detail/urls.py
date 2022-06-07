from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('detail/', views.show_detail_view, name='detail-page'),
    path('detail/<int:id>', views.animation_detail, name='animation_detail'),
    path('comment/<int:id>', views.comment, name='comment'),
    path('comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('bookmark/', views.comment, name='comment'),
    path('bookmark/delete/<int:id>', views.delete_comment, name='delete-comment'),
    path('recommend_toggle/<int:id>', views.recommend_toggle, name='recommend_toggle'),
]
