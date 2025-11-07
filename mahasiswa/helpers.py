from django.core.paginator import Paginator
from .models import Mahasiswa

def get_filtered_sorted_paginated_mahasiswa(request, items_per_page=10):
    """
    Helper function to filter, sort, and paginate Mahasiswa queryset
    
    Args:
        request: Django request object
        items_per_page: Number of items per page (default 10)
        
    Returns:
        tuple: (page_obj, filters_dict)
    """
    mahasiswa_list = Mahasiswa.objects.all()

    # --- FILTER ---
    fakultas = request.GET.get('fakultas')
    status = request.GET.get('status')

    if fakultas and fakultas != "All":
        mahasiswa_list = mahasiswa_list.filter(fakultas=fakultas)
    if status and status != "All":
        mahasiswa_list = mahasiswa_list.filter(status=status)

    # --- SORT ---
    sort_by = request.GET.get('sort')
    if sort_by in ['nim', 'nama_lengkap', 'ipk', 'angkatan']:
        mahasiswa_list = mahasiswa_list.order_by(sort_by)
    else:
        mahasiswa_list = mahasiswa_list.order_by('nim')  # default

    # --- PAGINATION ---
    paginator = Paginator(mahasiswa_list, items_per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj, {
        'fakultas_selected': fakultas or "All",
        'status_selected': status or "All",
        'sort_selected': sort_by or ""
    }

def get_mahasiswa_context(request, items_per_page=10):
    """
    Returns a context dictionary for admin dashboard with filtered, sorted, and paginated results
    
    Args:
        request: Django request object
        items_per_page: Number of items per page (default 10)
        
    Returns:
        tuple: (page_obj, context_dict)
    """
    page_obj, filters = get_filtered_sorted_paginated_mahasiswa(request, items_per_page)
    
    context = {
        'page_obj': page_obj,
        'fakultas_selected': filters['fakultas_selected'],
        'status_selected': filters['status_selected'],
        'sort_selected': filters['sort_selected'],
    }
    
    return page_obj, context