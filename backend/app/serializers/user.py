from app.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    firstname = serializers.CharField(max_length=10)
    lastname = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    country = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=4)
    phone = serializers.CharField(max_length=15)

    experience = serializers.ChoiceField(choices=User.Experience.choices)

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'country', 'email', 'code', 'phone', 'experience']
