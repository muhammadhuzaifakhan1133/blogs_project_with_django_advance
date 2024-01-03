from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "password", "confirm_password"]

    def validate(self, attrs):
        data = super().validate(attrs)
        print(data)
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError({"password": "password & confirm_password does not match"})
        return data

    def save(self, **kwargs):
        if "confirm_password" in self.validated_data:
            self.validated_data.pop("confirm_password")
        return super().save(**kwargs)
    
class UserListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]