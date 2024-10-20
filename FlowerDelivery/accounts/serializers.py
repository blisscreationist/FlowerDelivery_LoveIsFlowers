from rest_framework import serializers

class UserCheckSerializer(serializers.Serializer):
    exists = serializers.BooleanField()
    user_id = serializers.IntegerField(allow_null=True)