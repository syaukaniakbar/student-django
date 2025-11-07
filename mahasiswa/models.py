from django.db import models
from university.models import User

# Create your models here.

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=20, unique=True)
    nama_lengkap = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=1, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    jurusan = models.CharField(max_length=100)
    fakultas = models.CharField(max_length=100)
    angkatan = models.PositiveIntegerField()
    ipk = models.DecimalField(max_digits=3, decimal_places=2)
    sks_lulus = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=[
        ('Aktif', 'Aktif'),
        ('Cuti', 'Cuti'),
        ('Lulus', 'Lulus'),
        ('Drop Out', 'Drop Out'),
    ])
    alamat = models.TextField()
    kota = models.CharField(max_length=100)
    provinsi = models.CharField(max_length=100)
    no_telepon = models.CharField(max_length=20)
    nama_wali = models.CharField(max_length=100)
    no_telepon_wali = models.CharField(max_length=20)
    # Add a user field to link to the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nim} - {self.nama_lengkap}"