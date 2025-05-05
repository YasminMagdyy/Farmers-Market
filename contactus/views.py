from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'contactus/contact.html', {'form': form})

# Placeholder views for other pages
def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def products(request):
    return render(request, 'product.html')
def blog(request):
    return render(request, 'blog.html')
def features(request):
    return render(request, 'feature.html')
def testimonial(request):
    return render(request, 'testimonial.html')
def not_found(request):
    return render(request, '404.html')