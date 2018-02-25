from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from . import models
from . import forms


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:view_profile')  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )

    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:edit_profile'))

    return render(request, 'accounts/sign_up.html', {'form': form})


def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))


@login_required
def view_profile(request):
    user = get_object_or_404(models.User, pk=request.user.id)
    profile = user.userprofile

    return render(request, 'accounts/user_profile.html',
                  {'profile': profile})


@login_required
def edit_profile(request):
    user = get_object_or_404(models.User, pk=request.user.id)
    profile = user.userprofile

    form = forms.UserProfileForm()

    if request.method == 'POST':
        form = forms.UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved successfully!')
            return HttpResponseRedirect(reverse('accounts:view_profile'))
    else:
        form = forms.UserProfileForm(instance=request.user.userprofile)

    return render(request, 'accounts/user_profile.html', {'form': form,
                                                          'profile': profile})


@login_required
def change_password(request):
    user = get_object_or_404(models.User, pk=request.user.id)
    form = forms.ChangePasswordForm()

    if request.method == 'POST':
        if user.check_password(request.POST['current_password']):
            if request.POST['new_password'] == \
                    request.POST['confirm_new_password']:
                user.set_password(request.POST['new_password'])
                user.save()
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(
                    request, 'Passwords must match, please try again.')
        else:
            messages.error(request, 'Current password is incorrect')

    return render(request, 'accounts/change_password.html', {'form': form})
