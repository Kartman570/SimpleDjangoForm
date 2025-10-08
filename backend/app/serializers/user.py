"""
Serializer for the User model.
Validate input and define structure of user data.
"""
from rest_framework import serializers

from app.models import User


class UserSerializer(serializers.ModelSerializer):
    """Length limitation are picked for example. Approval from the PM is required"""

    firstname = serializers.CharField(max_length=10)
    lastname = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    country = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=4)
    phone = serializers.CharField(max_length=15)

    experience = serializers.ChoiceField(choices=User.Experience.choices)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'email', 'country', 'code', 'phone', 'experience']
