from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def save(self, *args, **kwargs):
        # Prevent admin users from having a profile
        if not self.user.is_superuser:
            super().save(*args, **kwargs)

class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    problem = models.CharField(max_length=255)
    document = models.FileField(upload_to='medical_documents/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

