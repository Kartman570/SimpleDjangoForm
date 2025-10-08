"""
Defines the User model.
Used only for validation - no real database persistence.
"""
from django.db import models


class User(models.Model):
    """Length limitation are picked for example. Approval from the PM is required"""
    class Experience(models.TextChoices):
        LOW = "low", "low"
        MEDIUM = "medium", "medium"
        HIGH = "high", "high"

    firstname = models.TextField(max_length=10)
    lastname = models.TextField(max_length=20)
    email = models.TextField()

    country = models.TextField(max_length=20)
    code = models.TextField(max_length=4)
    phone = models.TextField(max_length=15)

    experience = models.CharField(choices=Experience)
