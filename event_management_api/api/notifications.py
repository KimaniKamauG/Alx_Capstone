from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from datetime import timedelta
from django.utils import timezone

class EventNotifications:
    """
    Handles all email notifications related to events
    """
    @staticmethod
    def send_registration_confirmation(user, event):
        """Send confirmation email when user registers for an event"""
        subject = f'Registration Confirmed: {event.title}'
        context = {
            'user': user,
            'event': event,
        }
        message = render_to_string('emails/registration_confirmation.html', context)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
        )

    @staticmethod
    def send_event_reminder(registration):
        """Send reminder email 24 hours before event"""
        subject = f'Reminder: {registration.event.title} is tomorrow!'
        context = {
            'user': registration.user,
            'event': registration.event,
        }
        message = render_to_string('emails/event_reminder.html', context)
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [registration.user.email],
            html_message=message,
        )