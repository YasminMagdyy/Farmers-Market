from django.shortcuts import render, redirect
from .models import Blog, Subscriber
from contactus.models import Event
from django.contrib import messages
from .forms import SubscribeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.core import serializers
from eventHandler.tasks import update_event_statuses
from django.shortcuts import get_object_or_404

def home(request):
    current_time = timezone.now()
    ads = Event.objects.filter(ad=True, endDate__gte=current_time)
    ads_list = [{
        'eventName': ad.eventName,
        'eventDescription': ad.eventDescription,
        'startDate': ad.startDate.isoformat(),
        'endDate': ad.endDate.isoformat(),
        'eventRegistrationStatus': ad.eventRegistrationStatus
    } for ad in ads]
    
    blogs = Blog.objects.all()
    return render(request, 'blogs/home.html', {
        'blogs': blogs,
        'ads': ads,
        'ads_json': json.dumps(ads_list)  # Convert to JSON string
    })

def blog_list(request): 
    blogs = Blog.objects.all().order_by('-created_date')
    selected_category = request.GET.get('category')
    selected_date = request.GET.get('date')
    
    # Apply filters
    if selected_category in ['ceremony', 'visit']:
        blogs = blogs.filter(category=selected_category)
    
    if selected_date:
        try:
            # Convert the date string to a date object
            from datetime import datetime
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
            blogs = blogs.filter(created_date=date_obj)
        except (ValueError, TypeError):
            # Handle invalid date format
            pass
    
    # Get all unique dates for the filter sidebar
    all_dates = Blog.objects.dates('created_date', 'day', order='DESC')
    
    # Get all visit blogs for the sidebar
    visit_blogs = Blog.objects.filter(category='visit').order_by('-created_date')
    
    # Get all ceremony blogs for the sidebar
    ceremony_blogs = Blog.objects.filter(category='ceremony').order_by('-created_date')
    
    return render(request, 'blogs/blog_list.html', {
        'blogs': blogs,
        'selected_category': selected_category,
        'selected_date': selected_date,
        'all_dates': all_dates,
        'visit_blogs': visit_blogs,
        'ceremony_blogs': ceremony_blogs
    })

def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    
    # Get related blogs by category only (tags removed)
    related_blogs = Blog.objects.filter(
        category=blog.category
    ).exclude(
        pk=blog.pk
    ).order_by('-created_date')
    
    # Limit to 6 related blogs for better display
    related_blogs = related_blogs[:6]
    
    context = {
        'blog': blog,
        'related_blogs': related_blogs,
    }
    return render(request, 'blogs/blog_detail.html', context)

@login_required
@require_POST
def toggle_save_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user in blog.saved_by.all():
        blog.saved_by.remove(request.user)
        saved = False
    else:
        blog.saved_by.add(request.user)
        saved = True
    return JsonResponse({'saved': saved})

@login_required
def saved_blogs(request):
    saved_blogs = request.user.saved_blogs.all().order_by('-created_date')
    return render(request, 'blogs/saved_blogs.html', {'saved_blogs': saved_blogs})


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
                messages.success(request, 'تمام! تم حفظ بريدك بنجاح 😊')
            else:
                messages.info(request, 'هذا البريد مسجل بالفعل.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')

@require_POST
def toggle_notify(request):
    subscriber = Subscriber.objects.get(email=request.user.email)
    subscriber.notify = not subscriber.notify
    subscriber.save()
    return JsonResponse({'success': True, 'notify': subscriber.notify})

def get_ads(request):
    current_time = timezone.now()
    ads = Event.objects.filter(ad=True, endDate__gte=current_time)
    ads_json = serializers.serialize('json', ads)
    return render(request, 'blogs/base.html', {'ads': ads, 'ads_json': ads_json})
# blogs/views.py

# views.py
from django.utils import timezone

def get_current_ads(request):
    ads = Event.objects.filter(ad=True, eventRegistrationStatus= 'OPEN_FOR_REGISTRATION').order_by('-startDate')
    ad_data = [{
        'name': ad.eventName,
        'desc': ad.eventDescription,
        'start': timezone.localtime(ad.startDate).strftime('%Y-%m-%d %H:%M'),
        'end': timezone.localtime(ad.endDate).strftime('%Y-%m-%d %H:%M'),
        'status': ad.eventRegistrationStatus
    } for ad in ads]
    return JsonResponse({'ads': ad_data})

