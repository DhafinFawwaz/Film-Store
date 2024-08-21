from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client
from django.core.files.base import File
import mimetypes

class SupabaseStorage(Storage):
    def __init__(self, bucket_name="film-store-storage", **kwargs):
        print("Initializing SupabaseStorage...")
        self.bucket_name = bucket_name
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def _open(self, name, mode="rb"):
        pass

    def _save(self, name, content: File):
        print(f"Uploading {name} to bucket...")
        content_file = content.file
        content_file.seek(0)
        content_bytes = content_file.read()
        content_type, _ = mimetypes.guess_type(content.name)
        data = self.supabase.storage.from_(self.bucket_name).upload(
            name, content_bytes, {"content-type": content_type}
        )
        print(f"Successfully uploaded {name} to bucket.")
        return data.json()["Key"]

    def exists(self, name):
        pass

    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{name}"
    
    def delete(self, name):
        name = name.replace("film-store-storage/", "")
        print(f"Deleting {name} from bucket...")
        self.supabase.storage.from_(self.bucket_name).remove(name)
        print(f"Successfully deleted {name} from bucket.")