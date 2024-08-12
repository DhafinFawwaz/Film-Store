from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client

class SupabaseStorage(Storage):
    def __init__(self, bucket_name="film-store-storage", **kwargs):
        self.bucket_name = bucket_name
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

    def _open(self, name, mode="rb"):
        pass

    def _save(self, name, content):
        print("Uploading to bucket...")
        content_file = content.file
        content_file.seek(0)
        content_bytes = content_file.read()
        data = self.supabase.storage.from_(self.bucket_name).upload(
            name, content_bytes, {"content-type": content.content_type}
        )
        print("Successfully uploaded to bucket.")
        return data.json()["Key"]

    def exists(self, name):
        pass

    def url(self, name):
        return f"{settings.SUPABASE_URL}/storage/v1/object/public/{name}"
    
    def delete(self, name):
        print("Deleting from bucket...")
        self.supabase.storage.from_(self.bucket_name).remove(name)
        print("Successfully deleted from bucket.")