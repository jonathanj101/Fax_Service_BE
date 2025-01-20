from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone
import uuid

# need to add company_id where the fax belongs to


class TemporaryFilesModel(models.Model):
    file = models.FileField(upload_to="uploads/")
    business_id = models.UUIDField(
        primary_key=False, default=uuid.uuid4, editable=True)
    presigned_url = models.CharField(max_length=2000, null=True)
    file_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Temporary File: {self.file.name}"
