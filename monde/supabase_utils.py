from supabase import create_client
from django.conf import settings
from uuid import uuid4

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

import mimetypes

def upload_image_to_supabase(file, folder="uploads"):
    filename = f"{folder}/{uuid4().hex}_{file.name}"
    file_content = file.read()

    content_type = file.content_type
    if not content_type:
        content_type, _ = mimetypes.guess_type(file.name)
        if not content_type:
            content_type = "application/octet-stream"

    res = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        path=filename,
        file=file_content,
        file_options={"content-type": content_type}
    )

    if res.get("error"):
        raise Exception(f"Upload failed: {res['error']['message']}")

    return supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(filename)

