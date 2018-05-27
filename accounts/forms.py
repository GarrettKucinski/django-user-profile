import re
from django.contrib.auth.forms import PasswordChangeForm
from django.forms import ValidationError
from django.utils.html import escape
from django import forms
from datetime import datetime
from . import models


def validate_min_length(value):
    if not len(value) >= 10:
        raise forms.ValidationError(
            'You must enter 10 or more characters. currently: {}'.format(
                len(value)))


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea,
                          validators=[validate_min_length])
    date_of_birth = forms.DateField(
        input_formats=["%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"],
        error_messages={
            'invalid': 'Your birthday must be in one of the'
            ' following formats: mm/dd/yy, mm/dd/yyyy, yyyy-mm-dd'})

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

    def clean(data):
        cleaned_data = super().clean()
        email = cleaned_data['email']
        confirm_email = cleaned_data['confirm_email']
        bio = escape(cleaned_data.get('bio'))

        if email is None or confirm_email is None:
            raise forms.ValidationError('You must enter your email')

        if email != confirm_email:
            raise forms.ValidationError('Both emails must be the same!')


class ChangePasswordForm(PasswordChangeForm):

    def clean(self):
        old_password = self.data.get('old_password')
        new_password = self.data.get('new_password1')
        confirm_new_password = self.data.get('new_password2')

        if self.user.username in new_password:
            raise ValidationError('Password cannot contain your username')

        if not re.search(r'[A-Z]+', new_password):
            raise ValidationError(
                'Password must contain at least one uppercase character')

        if (self.user.userprofile.first_name in new_password or
                self.user.userprofile.last_name in new_password):
            raise ValidationError(
                'Your new password must not contain parts of your name.')

        if not re.search('[0-9]+', new_password):
            raise ValidationError(
                'Your password must contain at least one number')

        if not re.search('[!@#$]+', new_password):
            raise ValidationError(
                'Your password must contain at least one special character.'
                ' Allowed characters are @$#!')

        if len(new_password) < 14:
            raise ValidationError('Your password must be longer 14 characters')

        if old_password == new_password:
            raise ValidationError(
                'Your password cannot be the same as your old password')
