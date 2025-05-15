from django.urls import path
from . import views

app_name = "about_us"

urlpatterns = [
    path('about_us/',views.about_us, name ='about_us'),
    path('famers/', views.imp_farmers, name='farmers'),
    path('team/', views.farmers, name='team'),
    path('about-us/teambook/', views.teambook, name='teambook'),
]