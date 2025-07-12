from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User = get_user_model()

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'