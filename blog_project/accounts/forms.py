# accounts/forms.py
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
import re

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least one lowercase letter.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('Password must contain at least one special character.')
        if len(password) < 8:
            raise ValidationError('Password must be at least 8 characters long.')
        return password
