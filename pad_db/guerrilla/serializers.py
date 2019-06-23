from rest_framework import serializers

from .models import GuerrillaDungeon


class GuerillaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuerrillaDungeon
        fields = '__all__'
