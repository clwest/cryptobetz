from rest_framework import serializers
from .models import Coindesk

class CoindeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coindesk
        fields = '__all__'
