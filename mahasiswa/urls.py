from django.urls import path
from . import views
from .views_auth import login_view, logout_view

urlpatterns = [
    # Authentication URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # Dashboard URLs
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/admin/create/', views.mahasiswa_create, name='mahasiswa_create'),
    path('dashboard/admin/store/', views.mahasiswa_store, name='mahasiswa_store'),
    path('dashboard/admin/update/<int:pk>/', views.mahasiswa_update, name='mahasiswa_update'),
    path('dashboard/admin/delete/<int:pk>/', views.mahasiswa_delete, name='mahasiswa_delete'),
    path('dashboard/admin/<str:nim>/', views.mahasiswa_detail, name='mahasiswa_detail'),

    path('dashboard/mahasiswa/', views.mahasiswa_dashboard, name='mahasiswa_dashboard'),
    path('dashboard/mahasiswa/search/', views.search_mahasiswa, name='search_mahasiswa'),
    

]
