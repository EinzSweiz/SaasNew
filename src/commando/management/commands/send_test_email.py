from django.core.management.base import BaseCommand
from cfehome.tasks import send_email_task

class Command(BaseCommand):
    help = 'Send Test Email'
    def handle(self, *args, **kwargs):
        subject = 'Registration Success'
        message = 'Thank you so much for registration! Everything passed successfully!'
        recipient_list = ['riad.sultanov.1999@gmail.com'] 
        result = send_email_task(subject, message, recipient_list)
        self.stdout.write(self.style.SUCCESS(f'Test email task was sent'))