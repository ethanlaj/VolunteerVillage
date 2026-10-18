"""Private Google Cloud Storage for profile pictures (no Firebase SDK)."""

import base64
from datetime import timedelta
from functools import lru_cache
import json
import os
from urllib.parse import quote

from google.cloud import storage
from google.oauth2 import service_account


@lru_cache(maxsize=1)
def picture_bucket():
    info = json.loads(base64.b64decode(os.environ['GCS_SERVICE_ACCOUNT_BASE64']))
    credentials = service_account.Credentials.from_service_account_info(info)
    client = storage.Client(project=info['project_id'], credentials=credentials)
    return client.bucket(os.environ['GCS_PROFILE_BUCKET'])


def picture_key(user_id):
    if not user_id or '/' in user_id or '\\' in user_id:
        raise ValueError('Invalid profile picture user ID')
    return f'profile_pictures/{user_id}'


def profile_picture_url(user_id):
    picture_key(user_id)
    base_url = os.environ['PUBLIC_API_URL'].rstrip('/')
    return f'{base_url}/profile/picture/{quote(user_id, safe="")}'


def upload_profile_picture(file_path, user_id, content_type=None):
    blob = picture_bucket().blob(picture_key(user_id))
    blob.upload_from_filename(file_path, content_type=content_type)
    return profile_picture_url(user_id)


def signed_profile_picture_url(user_id):
    blob = picture_bucket().blob(picture_key(user_id))
    return blob.generate_signed_url(
        version='v4', expiration=timedelta(minutes=15), method='GET'
    )
