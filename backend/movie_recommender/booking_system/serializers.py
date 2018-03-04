from rest_framework import serializers

from .models import Cast


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ('name', 'age', 'description', 'gender', 'url', 'cast_type')
