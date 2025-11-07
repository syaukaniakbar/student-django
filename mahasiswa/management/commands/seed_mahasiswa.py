import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mahasiswa.models import Mahasiswa

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with mahasiswa data from JSON file and create associated user accounts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='mahasiswa/mahasiswa_data.json',
            help='Path to the JSON file containing mahasiswa data'
        )

    def handle(self, *args, **options):
        file_path = options['file']
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                mahasiswa_data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'File {file_path} not found')
            )
            return
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f'Invalid JSON in file {file_path}')
            )
            return

        created_count = 0
        skipped_count = 0
        
        for data in mahasiswa_data:
            # Check if user with this email already exists
            # Handle the case where some records might have 'nama_legkap' instead of 'nama_lengkap'
            nama_lengkap = data.get('nama_lengkap', data.get('nama_lengkap', ''))
            if not nama_lengkap:
                nama_lengkap = data.get('nama', '')  # In case there are other variations
            
            first_name = ''
            last_name = ''
            
            if nama_lengkap:
                name_parts = nama_lengkap.split()
                first_name = name_parts[0] if name_parts else ''
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
            
            # Create a username based on first and last name combination
            username = f"{first_name.lower()}.{last_name.lower().replace(' ', '')}".strip('.')
            if not username or username == '.':
                # Fallback to using email if name combination doesn't work
                username = data['email']
            
            user, created = User.objects.get_or_create(
                email=data['email'],
                defaults={
                    'username': username,
                    'email': data['email'],
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': 'mahasiswa',
                }
            )
            
            # Set password to 'mahasiswa' for all users
            user.set_password('mahasiswa')
            user.save()
            
            # Check if mahasiswa already exists with this NIM
            mahasiswa, created = Mahasiswa.objects.get_or_create(
                nim=data['nim'],
                defaults={
                    'nama_lengkap': nama_lengkap,
                    'email': data['email'],
                    'tanggal_lahir': data.get('tanggal_lahir'),
                    'jenis_kelamin': data.get('jenis_kelamin', ''),
                    'jurusan': data.get('jurusan', ''),
                    'fakultas': data.get('fakultas', ''),
                    'angkatan': data.get('angkatan', 0),
                    'ipk': data.get('ipk', 0),
                    'sks_lulus': data.get('sks_lulus', 0),
                    'status': data.get('status', 'Aktif'),
                    'alamat': data.get('alamat', ''),
                    'kota': data.get('kota', ''),
                    'provinsi': data.get('provinsi', ''),
                    'no_telepon': data.get('no_telepon', ''),
                    'nama_wali': data.get('nama_wali', ''),
                    'no_telepon_wali': data.get('no_telepon_wali', ''),
                    'user': user
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created mahasiswa: {nama_lengkap} (NIM: {data["nim"]})')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Skipped existing mahasiswa: {nama_lengkap} (NIM: {data["nim"]})')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Seeding completed: {created_count} created, {skipped_count} skipped'
            )
        )