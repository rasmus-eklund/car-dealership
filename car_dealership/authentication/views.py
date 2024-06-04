from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, EditProfileForm
from cars.models import Reservation

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile_view(request, profile_id=None):
    if profile_id:
        user = get_object_or_404(User, id=profile_id)
    else:
        user = request.user

    if request.user.is_superuser or request.user == user:
        if request.method == 'POST':
            form = EditProfileForm(request.POST, instance=user, user=user)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True})
            else:
                errors = {field: error.get_json_data()
                          for field, error in form.errors.items()}
                return JsonResponse({'success': False, 'errors': errors})
        else:
            form = EditProfileForm(instance=user, user=user)
    reservations = Reservation.objects.filter(user=user).all()

    return render(request, 'profile.html', {'form': form, 'user': user, 'current_user': request.user, 'reservations': reservations})

def logout_view(request):
    logout(request)
    return redirect('index')

