# blogs/context_processors.py
from django.utils import timezone
from contactus.models import Event  # Or eventHandler.models if you've moved them

def ads_processor(request):
    """
    Context processor for global ad banners.
    Adds upcoming events marked as ads to all templates.
    """
    context = {}
    
    try:
        # Get current time in correct timezone
        now = timezone.localtime(timezone.now())
        
        # Get active ads (events marked as ads that haven't ended yet)
        context['global_ads'] = Event.objects.filter(
            ad=True,
            endDate__gte=now
        ).order_by('startDate')[:5]  # Limit to 5 ads
        
        # Debug info (remove in production)
        context['ads_debug'] = {
            'server_time': now,
            'ads_count': context['global_ads'].count()
        }
        
    except Exception as e:
        # Fail silently but log errors
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in ads_processor: {str(e)}")
        context['global_ads'] = []
    
    return context