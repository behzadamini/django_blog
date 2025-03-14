from . import models
from django.forms import ModelForm, TextInput, EmailInput, Textarea

class ContactForm(ModelForm):
    class Meta:
        model = models.contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {
            'name': 'Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Message',
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name', 'required': False}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email', 'required': False}),
            'subject': TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject', 'required': False}),
            'message': Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        
        self.fields['subject'].required = False

        
        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages = {'required': ''}
                field.label = f"{field.label} *"