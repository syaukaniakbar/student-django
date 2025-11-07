from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mahasiswa.models import Mahasiswa

User = get_user_model()

class Command(BaseCommand):
    help = 'Create initial admin and mahasiswa users for testing'

    def handle(self, *args, **options):
        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@development.com',
                'first_name': 'System',
                'last_name': 'Administrator',
                'role': 'admin',
                'is_staff': False,  # Explicitly set to False to avoid Django admin redirect
                'is_superuser': False  # Explicitly set to False to avoid Django admin redirect
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Successfully created admin user: admin / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user already exists')
            )

