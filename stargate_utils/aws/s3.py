from mimetypes import MimeTypes
from botocore.client import Config
import boto3
from django.conf import settings
def get_file_content_type(filename):
    mime = MimeTypes()
    content_type = mime.guess_type(filename)[0]
    if content_type:
        if content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            return 'binary/octet-stream'
        return content_type
    return 'binary/octet-stream'


def upload_object(data, type, uuid):
    if type not in ['photo', 'resume']:
        raise Exception("Invalid upload object")
    content_type = get_file_content_type(data.name)
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    key = '{}student/{}/{}/{}'.format(settings.SERVER_ENV,uuid, type, data.name)
    object_location = '{}{}'.format(settings.S3_BASE_URL, key)
    bucket = s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
    object = bucket.put_object(Key=key,Body=data,  ContentType=content_type)

    return object_location

