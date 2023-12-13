import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_superuser", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(username, password, **other_fields)

    def create_user(self, username, password, **other_fields):
        if not username:
            raise ValueError(_("You must provide an username"))
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class ChatUser(AbstractBaseUser, PermissionsMixin):
    """user model"""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    need_password_change = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    designation = models.CharField(
        verbose_name="Designation", max_length=30, blank=True, null=True
    )
    username = models.CharField(
        verbose_name="Username", max_length=30, blank=True, unique=True, null=True
    )
    full_name = models.CharField(
        verbose_name="Full Name", max_length=30, blank=True, null=True
    )
    timestamp = models.DateTimeField(auto_now=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        permissions = [
            ("custom_profile_delete_users", "Can delete  users"),
            ("custom_profile_add_users", "Can add  users"),
            ("custom_profile_view_users", "Can view  users"),
            ("custom_profile_edit_users", "Can edit  users"),
        ]
        ordering = ["-timestamp"]
