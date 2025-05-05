from django.shortcuts import render
from .models import Blog

def home(request):
    blogs = Blog.objects.all()  # Fetch all blogs for the featured section
    return render(request, 'blogs/home.html', {'blogs': blogs})

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})