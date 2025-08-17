from django.shortcuts import render
from .models import Farmer, TeamMemebers

def about_us(requests):
    team = TeamMemebers.objects.all()
    return render(requests,'about_us/about_us.html',{"employees": team})

def imp_farmers(request):
    
    return render(request, 'about_us/imp_farmers.html', {})

def farmers(request):
        farmers = Farmer.objects.all()
        return render(request, 'about_us/farmers.html', {'farmers':farmers})

def teambook(request):
    return render(request, 'about_us/teambook.html', {})


# filers for product time
x = {"filters": {"product": "product.productName"}}