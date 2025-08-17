from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('blogs/', views.blog_list, name='blog_list'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('toggle-notify/', views.toggle_notify, name='toggle_notify'),
    path('', views.get_ads, name='home'),
    path('api/current-ads/',views. get_current_ads, name='current_ads'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)