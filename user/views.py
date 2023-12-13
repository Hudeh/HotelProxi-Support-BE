from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (
    LoginSerializer,
    RegisterUserSerializer,
    UserSerializer,
    ChangePasswordSerializer,
    GroupSerializer,
    PermissionSerializer,
)
from .models import ChatUser
from drf_yasg.utils import swagger_auto_schema


# register staff from tenant view
class RegisterHotelUserView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(operation_summary="Endpoint fto create user")
    def post(self, request):
        data = request.data
        full_name = (
            data["first_name"].capitalize() + " " + data["last_name"].capitalize()
        )
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(full_name=full_name)
            group = Group.objects.get(id=data["group"])
            user.groups.add(group)
            if user:
                return Response(
                    {
                        "status": True,
                        "msg": "User account created",
                    },
                    status=status.HTTP_201_CREATED,
                )
        return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)


# Login User for each domain tenant
class LogInView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary="Endpoint to login user")
    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Logout API
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(operation_summary="Endpoint for logout")
    def post(self, request):
        data = request.data
        user = ChatUser.objects.get(id=request.user.id)
        user.save()
        refresh_token = data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(
            {"success": True, "msg": "You now logged out"}, status=status.HTTP_200_OK
        )


# GET ALL USER
class MainUserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Endpoint for UserList")
    def get(self, request):
        users = ChatUser.objects.all()
        serializer = self.get_serializer(users, many=True)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# Edit User
class UpdateDeleteUser(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "patch", "delete"]
    serializer_class = UserSerializer

    def get(self, request, user_id):
        user = ChatUser.objects.get(id=user_id)
        serializer = self.get_serializer(user)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )

    def patch(self, request, user_id):
        data = request.data
        group = data["group"]
        full_name = (
            data["first_name"].capitalize() + " " + data["last_name"].capitalize()
        )

        group = Group.objects.get(id=group)

        user = ChatUser.objects.get(id=user_id)
        serializer = self.get_serializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save(full_name=full_name, designation=data["designation"])
            user.groups.add(group)
            return Response(
                {"status": True, "msg": "User account updated"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"status": False, "msg": "Error Updating Profile"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, user_id):
        user = ChatUser.objects.get(id=user_id)
        user.delete()
        return Response({"status": True}, status=status.HTTP_204_NO_CONTENT)


# GET USER
class MainUser(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_summary="Endpoint for Single User")
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


# Change Password API
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    @swagger_auto_schema(operation_summary="Endpoint to Chnage Password")
    def post(self, request):
        self.object = self.get_object()
        data = request.data
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"status": False, "msg": "Old Password Wrong!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.need_password_change = False
            self.object.save()
            response = {
                "status": True,
                "msg": "Password Updated Successfully",
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(
            {"status": False, "msg": "Error updating password"},
            status=status.HTTP_400_BAD_REQUEST,
        )


# group create and list
class GroupView(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    @swagger_auto_schema(operation_summary="Endpoint for Create Group")
    def create(self, request):
        data = request.data
        post_permission_id = data["checked"]
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            group = serializer.save()
            if group:
                for perm_id in post_permission_id:
                    perm = Permission.objects.get(id=perm_id)
                    group.permissions.add(perm)
                return Response(
                    {
                        "status": True,
                        "msg": "Group created",
                    },
                    status=status.HTTP_201_CREATED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        query = Group.objects.all()
        serializer = GroupSerializer(query, many=True)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )


class PermissionAPI(generics.ListAPIView):
    queryset = Permission.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionSerializer

    @swagger_auto_schema(operation_summary="Endpoint to list permissions")
    def list(self, request):
        app_labels = [
            "user",
            "chat",
        ]

        custom_permissions = Permission.objects.filter(
            content_type__app_label__in=app_labels, codename__startswith="custom_"
        )
        serializer = PermissionSerializer(custom_permissions, many=True)
        return Response(
            {"status": True, "data": serializer.data}, status=status.HTTP_200_OK
        )
