from .celery import app
from django.core.mail import send_mail
from django.conf import settings


@app.task
def send_email_task(subject, message, recipient_list):
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list,
            fail_silently=False
        )
        print('Email was sent successfully')
    except Exception as e:
        print(f'Failed to send email: {e}')
