from rest_framework import serializers
from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User

MIN_LENGTH  = 6


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = "__all__"



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=MIN_LENGTH, error_messages={
            "min_length": f"Password must be longer than {MIN_LENGTH} characters."
        })
    password2 = serializers.CharField(
        write_only=True, min_length=MIN_LENGTH, error_messages={
            "min_length": f"Password must be longer than {MIN_LENGTH} characters."
        })

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password does not match.")
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


