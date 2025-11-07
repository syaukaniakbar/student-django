from django.shortcuts import render, redirect, get_object_or_404
from .models import Mahasiswa
from .forms import MahasiswaForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import admin_required, mahasiswa_required
from .helpers import get_mahasiswa_context
from .utils.notifications import send_notification_to_topic
from .documents import MahasiswaDocument

# Dashboard views
@login_required
def admin_dashboard(request):
    # Use helper to get paginated and filtered results
    _, context = get_mahasiswa_context(request)
    return render(request, 'admin_dashboard.html', context)

@login_required
def mahasiswa_dashboard(request):
    return render(request, 'mahasiswa_dashboard.html')

# Detail Mahasiswa
@admin_required
def mahasiswa_detail(request, nim):
    mhs = get_object_or_404(Mahasiswa, nim=nim)
    return render(request, 'mahasiswa_detail.html', {'object': mhs})

# Create Mahasiswa - Show Form
@admin_required
def mahasiswa_create(request):
    form = MahasiswaForm()
    return render(request, 'mahasiswa_form.html', {'form': form})

# Store Mahasiswa - Process Form Data
@admin_required
def mahasiswa_store(request):
    if request.method == 'POST':
        form = MahasiswaForm(request.POST)
        if form.is_valid():
            mahasiswa = form.save()
            # Kirim notifikasi setelah create berhasil
            response = send_notification_to_topic(
                title="Mahasiswa Baru Ditambahkan",
                body=f"Data mahasiswa {mahasiswa.nama_lengkap} telah berhasil ditambahkan ke sistem",
                topic='mahasiswa_updates'
            )
            if response:
                messages.success(request, f"Data mahasiswa {mahasiswa.nama_lengkap} telah berhasil ditambahkan dan notifikasi telah dikirim.")
            else:
                messages.warning(request, f"Data mahasiswa {mahasiswa.nama_lengkap} telah berhasil ditambahkan tetapi notifikasi gagal dikirim.")
            return redirect('admin_dashboard')
    else:
        # If accessed via GET, redirect to the form
        return redirect('mahasiswa_create')

# Update Mahasiswa
@admin_required
def mahasiswa_update(request, pk):
    mhs = get_object_or_404(Mahasiswa, pk=pk)
    if request.method == 'POST':
        form = MahasiswaForm(request.POST, instance=mhs)
        if form.is_valid():
            mahasiswa = form.save()
            # Kirim notifikasi setelah update berhasil
            response = send_notification_to_topic(
                title="Data Mahasiswa Diupdate",
                body=f"Data mahasiswa {mahasiswa.nama_lengkap} telah berhasil diperbarui",
                topic='mahasiswa_updates'
            )
            if response:
                messages.success(request, f"Data mahasiswa {mahasiswa.nama_lengkap} telah berhasil diperbarui dan notifikasi telah dikirim.")
            else:
                messages.warning(request, f"Data mahasiswa {mahasiswa.nama_lengkap} telah berhasil diperbarui tetapi notifikasi gagal dikirim.")
            return redirect('admin_dashboard')
    else:
        form = MahasiswaForm(instance=mhs)
    return render(request, 'mahasiswa_form.html', {'form': form})

# Delete Mahasiswa
@admin_required
def mahasiswa_delete(request, pk):
    mhs = get_object_or_404(Mahasiswa, pk=pk)
    if request.method == 'POST':
        nama_mahasiswa = mhs.nama_lengkap  # Simpan nama sebelum dihapus
        mhs.delete()
        # Kirim notifikasi setelah delete berhasil
        response = send_notification_to_topic(
            title="Data Mahasiswa Dihapus",
            body=f"Data mahasiswa {nama_mahasiswa} telah berhasil dihapus dari sistem",
            topic='mahasiswa_updates'
        )
        if response:
            messages.success(request, f"Data mahasiswa {nama_mahasiswa} telah berhasil dihapus dan notifikasi telah dikirim.")
        else:
            messages.warning(request, f"Data mahasiswa {nama_mahasiswa} telah berhasil dihapus tetapi notifikasi gagal dikirim.")
        return redirect('admin_dashboard')
    return render(request, 'mahasiswa_confirm_delete.html', {'object': mhs})

def search_mahasiswa(request):
    q = request.GET.get('q')
    results = []
    if q:
        search_results = MahasiswaDocument.search().query(
            "multi_match",
            query=q,
            fields=['nama_lengkap', 'nim', 'jurusan', 'kota', 'fakultas']
        )
        # Dapatkan hasil pencarian
        search_response = search_results.execute()
        # Konversi hasil ke objek model Django asli agar bisa diakses dengan benar
        results = []
        for hit in search_response:
            # Dapatkan objek model asli berdasarkan ID dari hasil pencarian
            try:
                obj = Mahasiswa.objects.get(pk=hit.id)
                results.append(obj)
            except Mahasiswa.DoesNotExist:
                # Jika objek tidak ditemukan di database, lewati
                continue
    return render(request, 'search.html', {'results': results})