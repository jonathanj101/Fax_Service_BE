from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone
import uuid


class EmployeeModel(models.Model):
    # employee_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # need testing
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user_id = models.ForeignKey(
    #     "UserModel", on_delete=DO_NOTHING, null=False, default=""
    # )
    user_id = models.UUIDField(primary_key=False, default="", editable=False)
    # company_id = models.ForeignKey("CompanyModel", on_delete=DO_NOTHING, null=False)
    company_id = models.UUIDField(
        primary_key=False, default="", editable=False, null=False
    )
    timestamp = models.DateField(blank=True, default=timezone.now)

    def __str__(self):
        return (
            f"(`{self.id}`,`{self.user_id}`, `{self.company_id}`, `{self.timestamp}`)"
        )
