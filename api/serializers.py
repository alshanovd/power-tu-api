from rest_framework import serializers
from .models import PowerUser

class PowerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerUser
        fields = '__all__'


