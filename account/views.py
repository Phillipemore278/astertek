from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import CustomUserCreationForm


def register_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)  # Log user in immediately after registration
            messages.success(request, "Registration successful.")
            return redirect(next_url or 'account:dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/register.html', {
        'form': form,
        'next': next_url
    })


def custom_login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url or 'account:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'account/login.html', {'next': next_url})


def auth_choice_view(request):
    next_url = request.GET.get('next', '/')
    return render(request, 'account/auth_choice.html', {'next': next_url})
