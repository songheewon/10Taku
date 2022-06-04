from django.urls import path
from . import views

urlpatterns = [
    path('detail/', views.show_detail_view, name='detail'),
]
# from django.contrib import admin
# from django.urls import path, include
# from . import views
#
# urlpatterns = [
#     path('comment/<int:id>', views.comment, name='comment'),
#     path('comment/delete/<int:id>', views.delete_comment, name='delete-comment'),
#     path('bookmark/', views.comment, name='comment'),
#     path('bookmark/delete/<int:id>', views.delete_comment, name='delete-comment'),
#
# ]