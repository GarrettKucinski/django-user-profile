from django import forms
from django.utils.html import escape
from datetime import datetime
from . import models


def validate_min_length(value):
    if not len(value) >= 10:
        raise forms.ValidationError(
            'You must enter 10 or more characters. currently: {}'.format(
                len(value)))


def validate_date_format(value):
    date = str(value)

    try:
        datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        try:
            datetime.strptime(date, '%m/%d/%y')
        except ValueError:
            try:
                datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise forms.ValidationError(
                    ('''Your birthday must be in one of the following formats:
                     mm/dd/yy, mm/dd/yyyy, yyyy-mm-dd''')
                )


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea,
                          validators=[validate_min_length])
    date_of_birth = forms.CharField(validators=[validate_date_format])

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


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(max_length=255)
    new_password = forms.CharField(max_length=255)
    confirm_new_password = forms.CharField(max_length=255)
