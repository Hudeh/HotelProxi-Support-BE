from storages.backends.s3boto3 import S3Boto3Storage
from django_tenants.utils import parse_tenant_config_path


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"

    @property
    def location(self) -> str:
        _location = parse_tenant_config_path("%s")
        return _location


class PublicMediaStorage(S3Boto3Storage):
    location = "media"
    default_acl = "public-read"
    file_overwrite = False

    @property
    def location(self) -> str:
        _location = parse_tenant_config_path("%s")
        return _location


class PrivateMediaStorage(S3Boto3Storage):
    location = "private"
    default_acl = "private"
    file_overwrite = False
    custom_domain = False

    @property
    def location(self) -> str:
        _location = parse_tenant_config_path("%s")
        return _location
