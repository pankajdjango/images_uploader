from django.contrib.auth.decorators import login_required
from django.contrib import messages
from functools import wraps
from django.shortcuts import redirect
from .models import UserAccount
def hk_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return _wrapped_view

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        super_user = UserAccount.objects.filter(user_id=request.session.get("user_id"),is_staff=True).exists()
        if super_user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return _wrapped_view



def hk_or_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return login_required(view_func)(request, *args, **kwargs)
        elif 'user_id' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login')
    return _wrapped_view

def already_login(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated or 'user_id' in request.session:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view
