from django.core.management.base import BaseCommand
from polls.models import User, Question
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds the database with sample questions'

    def handle(self, *args, **kwargs):
        # Sample questions data
        sample_questions = [
            {
                'option_one': 'Have the ability to fly',
                'option_two': 'Have the ability to become invisible'
            },
            {
                'option_one': 'Travel to the past',
                'option_two': 'Travel to the future'
            },
            {
                'option_one': 'Be able to speak all languages',
                'option_two': 'Be able to talk to animals'
            },
            {
                'option_one': 'Live in the city',
                'option_two': 'Live in the countryside'
            },
            {
                'option_one': 'Have unlimited money',
                'option_two': 'Have unlimited time'
            },
            {
                'option_one': 'Be famous',
                'option_two': 'Be anonymous but wealthy'
            },
            {
                'option_one': 'Read minds',
                'option_two': 'Predict the future'
            },
            {
                'option_one': 'Always be 10 minutes late',
                'option_two': 'Always be 20 minutes early'
            },
            {
                'option_one': 'Give up social media',
                'option_two': 'Give up streaming services'
            },
            {
                'option_one': 'Have super strength',
                'option_two': 'Have super speed'
            }
        ]

        # Get all users (or create default users if none exist)
        users = list(User.objects.all())
        
        if not users:
            self.stdout.write(
                self.style.WARNING('No users found. Creating default users first...')
            )
            from django.core.management import call_command
            call_command('create_initial_users')
            users = list(User.objects.all())

        # Create questions
        created_count = 0
        for idx, q_data in enumerate(sample_questions):
            # Rotate through users
            author = users[idx % len(users)]
            
            # Check if question already exists
            existing = Question.objects.filter(
                option_one_text=q_data['option_one'],
                option_two_text=q_data['option_two']
            ).exists()
            
            if not existing:
                Question.objects.create(
                    author=author,
                    option_one_text=q_data['option_one'],
                    option_two_text=q_data['option_two']
                )
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created question: {q_data["option_one"]} or {q_data["option_two"]}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'Question already exists: {q_data["option_one"]} or {q_data["option_two"]}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} questions!')
        )
        
        total_questions = Question.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Total questions in database: {total_questions}')
        )