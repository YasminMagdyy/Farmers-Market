from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.http import require_POST

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blogs/<int:pk>/toggle-save/', require_POST(views.toggle_save_blog), name='toggle_save_blog'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('saved-blogs/', views.saved_blogs, name='saved_blogs'),
    path('toggle-notify/', views.toggle_notify, name='toggle_notify'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
