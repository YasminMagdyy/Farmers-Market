from django.shortcuts import render, redirect
from .models import Blog, Subscriber
from django.contrib import messages
from .forms import SubscribeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

def home(request):
    blogs = Blog.objects.all()  # Fetch all blogs for the featured section
    return render(request, 'blogs/home.html', {'blogs': blogs})

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs/blog_list.html', {'blogs': blogs})

def blog_detail(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    return render(request, 'blogs/blog_detail.html', {'blog': blog})


def subscribe_view(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            subscriber, created = form.save(commit=False), False
            try:
                subscriber = Subscriber.objects.get(email=form.cleaned_data['email'])
            except Subscriber.DoesNotExist:
                subscriber = form.save()
                created = True

            if created:
                messages.success(request, 'ٍSuccessfully Saved😊')
            else:
                messages.info(request, 'This mail is already registered.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@require_POST
def toggle_notify(request):
    subscriber = Subscriber.objects.get(email=request.user.email)
    subscriber.notify = not subscriber.notify
    subscriber.save()
    return JsonResponse({'success': True, 'notify': subscriber.notify})