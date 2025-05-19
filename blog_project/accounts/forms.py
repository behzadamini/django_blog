# accounts/forms.py
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError
import re

class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password1(self):
        password = self.cleaned_data.get('new_password1')
        if not re.search(r'[A-Z]', password):
            raise ValidationError('رمز عبور باید حداقل یک حرف بزرگ داشته باشد.')
        if not re.search(r'[a-z]', password):
            raise ValidationError('رمز عبور باید حداقل یک حرف کوچک داشته باشد.')
        if not re.search(r'[0-9]', password):
            raise ValidationError('رمز عبور باید حداقل یک عدد داشته باشد.')
        if not re.search(r'[\W_]', password):
            raise ValidationError('رمز عبور باید حداقل یک نماد داشته باشد.')
        if len(password) < 8:
            raise ValidationError('رمز عبور باید حداقل ۸ کاراکتر باشد.')
        return password
