from rest_framework import serializers

class PictureSerializer(serializers.Serializer):
    url = serializers.URLField()