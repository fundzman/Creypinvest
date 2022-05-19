from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class CachedS3BotoStorage(S3Boto3Storage):
    """
    S3BotoStorage backend which also saves a hashed copies of the files it saves.
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    custom_domain = settings.STATIC_URL


class MediaS3BotoStorage(S3Boto3Storage):
    """
    S3BotoStorage backend for media files.
    """
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    custom_domain = settings.MEDIA_URL


class StaticStorage(S3Boto3Storage):
    location = settings.STATIC_LOCATION
    default_acl = 'public-read'
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN


class PublicMediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    # custom_domain = settings.MEDIA_URL
    location = settings.PUBLIC_MEDIA_LOCATION
    default_acl = 'public-read'
    file_overwrite = True

# class PrivateMediaStorage(S3Boto3Storage):
#     location = settings.PRIVATE_MEDIA_LOCATION
#     default_acl = 'private'
#     file_overwrite = False
#     custom_domain = False
