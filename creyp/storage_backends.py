from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class R2StaticStorage(S3Boto3Storage):
    """
    Cloudflare R2 backend for static files, served from the CDN domain.
    """
    location = "static"
    default_acl = None
    file_overwrite = True
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    object_parameters = {
        "CacheControl": "public, max-age=86400",
    }


class R2MediaStorage(S3Boto3Storage):
    """
    Cloudflare R2 backend for user uploads, served from the CDN domain.
    """
    location = "media"
    default_acl = None
    # Keep unique names so a re-upload never serves a stale CDN-cached file
    file_overwrite = False
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    object_parameters = {
        "CacheControl": "public, max-age=3600",
    }
