from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect

def admin_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Check if user has role attribute and if role is 'admin'
        if hasattr(request.user, 'role') and request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Akses ditolak. Hanya admin yang dapat mengakses halaman ini.')
            return redirect('admin_dashboard')  # Redirect to dashboard instead of login
    return _wrapped_view

def mahasiswa_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        # Check if user has role attribute and if role is 'mahasiswa'
        if hasattr(request.user, 'role') and request.user.role == 'mahasiswa':
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, 'Akses ditolak. Hanya mahasiswa yang dapat mengakses halaman ini.')
            return redirect('mahasiswa_dashboard')  # Redirect to dashboard instead of login
    return _wrapped_view