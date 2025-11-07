from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password) 
        
        if user:
            login(request, user)
            # Redirect based on user role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'mahasiswa':
                return redirect('mahasiswa_dashboard')
        else:
            messages.error(request, 'Email atau password salah')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')