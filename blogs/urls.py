from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('toggle-notify/', views.toggle_notify, name='toggle_notify'),
]