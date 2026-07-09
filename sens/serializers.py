from rest_framework import serializers
from .models import sens

class sensSerializer(serializers.ModelSerializer):
    class Meta:
        model = sens
        fields = '__all__'