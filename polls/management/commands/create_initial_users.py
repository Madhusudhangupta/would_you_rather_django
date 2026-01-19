from django.core.management.base import BaseCommand
from polls.models import User


class Command(BaseCommand):
    help = 'Creates initial users for the application'

    def handle(self, *args, **kwargs):
        users_data = [
            {
                'username': 'alex',
                'email': 'alex@example.com',
                'first_name': 'Alex',
                'last_name': 'One'
            },
            {
                'username': 'bob',
                'email': 'bob@example.com',
                'first_name': 'Bob',
                'last_name': 'Two'
            },
            {
                'username': 'charles',
                'email': 'charles@example.com',
                'first_name': 'Charles',
                'last_name': 'Three'
            },
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name']
                }
            )
            
            if created:
                # Set a default password (change this in production)
                user.set_password('password123')
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created user: {user.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user.username}')
                )