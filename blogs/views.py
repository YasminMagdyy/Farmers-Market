from django.shortcuts import render, redirect
from .models import Blog, Subscriber, Event
from django.contrib import messages
from .forms import SubscribeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from django.core import serializers
from eventHandler.tasks import update_event_statuses, send_event_notifications

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

