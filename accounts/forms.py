from django import forms
from . import models


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = [
            'first_name',
            'last_name',
            'email',
            'confirm_email',
            'date_of_birth',
            'bio',
            'image',
        ]


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=255)
    new_password = forms.CharField(max_length=255)
    confirm_new_password = forms.CharField(max_length=255)
