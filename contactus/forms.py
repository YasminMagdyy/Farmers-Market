from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'name', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'id': 'subject', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'id': 'message', 'placeholder': 'Leave a message here', 'style': 'height: 200px'}),
        }