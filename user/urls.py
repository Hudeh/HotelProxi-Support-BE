from django.urls import path, re_path
from .views import *

urlpatterns = [
    path("create_user", RegisterHotelUserView.as_view(), name="create_user"),
    path("login", LogInView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("users_list", MainUserList.as_view(), name="users_list"),
    path("user", MainUser.as_view(), name="user"),
    path(
        "user/change_password",
        ChangePasswordView.as_view(),
        name="user/change_password",
    ),
    re_path(
        r"^edit-user/(?P<user_id>[\w-]+)$", UpdateDeleteUser.as_view(), name="edit-user"
    ),
    path("group", GroupView.as_view(), name="group"),
    path("permission_list", PermissionAPI.as_view(), name="permission_list"),
]
