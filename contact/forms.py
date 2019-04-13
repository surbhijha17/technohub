from django import forms

from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Your Name',}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'YourEmail@gmail.com'}),
            'content': forms.Textarea(attrs={'class': 'form-control','rows':'5',}),}
            
        fields=['name','email','content', ]
      
