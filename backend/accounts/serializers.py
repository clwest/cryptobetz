from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ('email', 'password', 'name')
    extra_kwargs = {'passwork': {'write_only': True, 'min_length': 8}}
    
  def create(self, validated_data):
    return CustomUser.objects.create_user(**validated_data)