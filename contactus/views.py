from django.shortcuts import render, redirect
from .forms import ContactForm, EventRegistrationForm
from django.contrib import messages
from .models import Event, Attendee, EventAttendee

def contact(request):
    contact_form = ContactForm()
    available_events = Event.objects.filter(eventRegistrationStatus="OPEN_FOR_REGISTRATION")
    
    if request.method == 'POST':
        if 'attendee_name' in request.POST:  # Event registration form
            # Handle event registration
            attendee_name = request.POST.get('attendee_name')
            attendee_phone = request.POST.get('attendee_phone')
            event_id = request.POST.get('event')
            
            try:
                # Validate required fields
                if not attendee_name or not attendee_phone or not event_id:
                    messages.error(request, 'Please fill in all required fields.')
                    return render(request, 'contactus/contact.html', {
                        'form': contact_form,
                        'available_events': available_events,
                    })
                
                # Get or create attendee
                attendee, created = Attendee.objects.get_or_create(
                    attendeeName=attendee_name,
                    phoneNumber=attendee_phone
                )
                
                # Get the event
                event = Event.objects.get(id=event_id)
                
                # Check if registration is still open
                if event.eventRegistrationStatus != "OPEN_FOR_REGISTRATION":
                    messages.error(request, 'Registration for this event is closed.')
                    return render(request, 'contactus/contact.html', {
                        'form': contact_form,
                        'available_events': available_events,
                    })
                
                # Create event registration (check if already exists)
                event_attendee, registration_created = EventAttendee.objects.get_or_create(
                    eventName=event,
                    attendeeName=attendee
                )
                
                if registration_created:
                    messages.success(request, f'Successfully registered for "{event.eventName}"! We will contact you with more details.')
                else:
                    messages.info(request, f'You are already registered for "{event.eventName}".')
                    
            except Event.DoesNotExist:
                messages.error(request, 'Selected event not found. Please try again.')
            except Exception as e:
                messages.error(request, 'Registration failed. Please try again later.')
                
        else:  # Contact form
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return redirect('contactus:contact')
            else:
                messages.error(request, 'Please correct the errors in the form.')
    
    context = {
        'form': contact_form,
        'available_events': available_events,
    }
    return render(request, 'contactus/contact.html', context)

def event_registration(request):
    """Separate view for event registration (if you want to use separate URLs)"""
    if request.method == 'POST':
        attendee_name = request.POST.get('attendee_name')
        attendee_phone = request.POST.get('attendee_phone')
        event_id = request.POST.get('event')
        
        try:
            # Validate required fields
            if not attendee_name or not attendee_phone or not event_id:
                messages.error(request, 'Please fill in all required fields.')
                return redirect('contactus:contact')
            
            # Get or create attendee
            attendee, created = Attendee.objects.get_or_create(
                attendeeName=attendee_name,
                phoneNumber=attendee_phone
            )
            
            # Get the event
            event = Event.objects.get(id=event_id)
            
            # Check if registration is still open
            if event.eventRegistrationStatus != "OPEN_FOR_REGISTRATION":
                messages.error(request, 'Registration for this event is closed.')
                return redirect('contactus:contact')
            
            # Create event registration
            event_attendee, registration_created = EventAttendee.objects.get_or_create(
                eventName=event,
                attendeeName=attendee
            )
            
            if registration_created:
                messages.success(request, f'Successfully registered for "{event.eventName}"! We will contact you with more details.')
            else:
                messages.info(request, f'You are already registered for "{event.eventName}".')
                
        except Event.DoesNotExist:
            messages.error(request, 'Selected event not found. Please try again.')
        except Exception as e:
            messages.error(request, 'Registration failed. Please try again later.')
    
    return redirect('contactus:contact')

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