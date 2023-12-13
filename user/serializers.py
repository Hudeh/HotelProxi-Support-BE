from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import ChatUser


# GROUP SERIALIZER
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


# PERMISSION SERIALIZER
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "codename"]


# CREATE USER SERIALIZER
class RegisterUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )

    def create(self, validated_data):
        # group = self.context["request"].data["group"]
        user = get_user_model().objects.create(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ["pk", "username", "password", "designation"]
        extra_kwargs = {"password": {"write_only": True}}


# user serializer


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "full_name",
            "timestamp",
            "need_password_change",
            "designation",
            "permissions",
            "groups",
        ]


# LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        if username is None:
            raise exceptions.ValidationError(
                {"success": False, "msg": "Username is required to login"}
            )
        if password is None:
            raise exceptions.ValidationError(
                {"success": False, "msg": "Password is required to log in."}
            )
        user = authenticate(**data)
        if user is None:
            raise exceptions.AuthenticationFailed(
                {"success": False, "msg": "Wrong Credentials"}
            )

        if not user.is_active:
            raise exceptions.ValidationError(
                {"success": False, "msg": "User is not active"}
            )
        refresh = RefreshToken.for_user(user)
        chat_user = ChatUser.objects.get(id=user.id)
        serializer = UserSerializer(chat_user)
        return {
            "status": True,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": serializer.data,
            "msg": "Login Successful",
        }


# CHANGE PASSWORD SERIALIZER


class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=True)
