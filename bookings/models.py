from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.CharField(max_length=10)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.date} at {self.time} ({self.get_status_display()})"

@receiver(post_save, sender=Booking)
def handle_booking_status_change(sender, instance, **kwargs):
    if instance.status == 'confirmed':
        send_confirmation_email(instance)
    elif instance.status == 'cancelled':
        send_cancellation_email(instance)
        instance.delete()


def send_confirmation_email(booking):
    feedback_form_link = 'https://forms.gle/LDRn7yQ5Qc33kkgn8'
    subject = 'Appointment Confirmation'
    message = (
        f'Dear {booking.user.username},\n\n'
        f'Your appointment on {booking.date} at {booking.time} has been confirmed.\n\n'
        f'To help us improve our services, please provide your feedback by filling out this form:\n'
        f'{feedback_form_link}\n\n'
        f'Thank you!'
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.email]

    send_mail(subject, message, from_email, recipient_list)


def send_cancellation_email(booking):
    subject = 'Appointment Cancellation'
    message = f'Dear {booking.user.username},\n\nYour appointment on {booking.date} at {booking.time} has been cancelled.\n\nThank you!'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [booking.user.email]

    send_mail(subject, message, from_email, recipient_list)
