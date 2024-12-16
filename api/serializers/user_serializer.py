from rest_framework import serializers
from api.models.user_model import UserModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["first_name", "last_name", "username","email", "role"]