from rest_framework import serializers
from .models import Profile


class ProfileSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'name',
            'updated_at', 'content', 'image',
        ]