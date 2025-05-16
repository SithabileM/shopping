import requests
from django.conf import settings

def upload_to_imagekit(file):
    url="https://upload.imagekit.io/api/v1/files/upload"
    payload= {
        'fileName': file.name,
        'publicKey': settings.IMAGEKIT_PUBLIC_KEY
    }
    response= requests.post(
        url,
        auth=(settings.IMAGEKIT_PRIVATE_KEY,''),
        files={'file':file},
        data=payload
    )
    return response.json()