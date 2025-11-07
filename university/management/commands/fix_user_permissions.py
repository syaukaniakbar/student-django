from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Fix user permissions - remove staff/superuser status from custom admin users'

    def handle(self, *args, **options):
        # Find all users and ensure they don't have staff/superuser permissions unless they should
        users = User.objects.all()
        
        for user in users:
            # If user's role is 'admin' in your custom role system, 
            # they shouldn't have is_staff=True to avoid Django admin redirect
            updated = False
            if user.role == 'admin' and (user.is_staff or user.is_superuser):
                user.is_staff = False
                user.is_superuser = False
                updated = True
            
            if updated:
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Updated user {user.username} permissions')
                )
        
        self.stdout.write(
            self.style.SUCCESS('User permissions updated successfully')
        )