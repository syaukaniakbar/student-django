from django import forms
from .models import Mahasiswa

class MahasiswaForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['nim', 'nama_lengkap', 'email', 'tanggal_lahir', 'jenis_kelamin', 'jurusan', 'fakultas', 'angkatan', 'ipk', 'sks_lulus', 'status', 'alamat', 'kota', 'provinsi', 'no_telepon', 'nama_wali', 'no_telepon_wali']
        widgets = {
            'nim': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
            'jurusan': forms.TextInput(attrs={'class': 'form-control'}),
            'fakultas': forms.TextInput(attrs={'class': 'form-control'}),
            'angkatan': forms.NumberInput(attrs={'class': 'form-control'}),
            'ipk': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sks_lulus': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'kota': forms.TextInput(attrs={'class': 'form-control'}),
            'provinsi': forms.TextInput(attrs={'class': 'form-control'}),
            'no_telepon': forms.TextInput(attrs={'class': 'form-control'}),
            'nama_wali': forms.TextInput(attrs={'class': 'form-control'}),
            'no_telepon_wali': forms.TextInput(attrs={'class': 'form-control'}),
        }