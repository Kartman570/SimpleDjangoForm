from django.db import models


class User(models.Model):
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
