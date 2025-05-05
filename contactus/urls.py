from django.urls import path
from . import views
app_name = 'contactus'
urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    path('blog/', views.blog, name='blog'),
    path('features/', views.features, name='features'),
    path('testimonial/', views.testimonial, name='testimonial'),
    path('404/', views.not_found, name='404'),
]