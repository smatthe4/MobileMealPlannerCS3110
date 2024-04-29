from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Profile

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            print('role', allowed_roles)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            else:
                return HttpResponse('You are not authorized to view this page')
            
        return wrapper_func
    return decorator

def user_is_owner():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            user = request.user
            
            profile = Profile.objects.get(user=user)

            if user == profile.user:
                return view_func(request, *args, **kwargs)
            else:
                messages.warning(request, 'You are not authorized to view this page')
                return redirect('index')
        return wrapper_func
    return decorator