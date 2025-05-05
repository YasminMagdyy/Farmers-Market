from django.shortcuts import render

def about_us(requests):
    return render(requests,'about_us/about_us.html',{})

def imp_farmers(request):
    return render(request, 'about_us/imp_farmers.html', {})