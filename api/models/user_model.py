from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone
import uuid

class UserModel(models.Model):
    first_name = models.CharField(max_length=100,null=False)
    middle_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100,null=False)
    username = models.CharField(max_length=25,null=False, unique=True)
    password = models.CharField(max_length=200,null=False)
    email = models.CharField(max_length=100,null=False,unique=True)
    timestamp = models.DateField(blank=True,default=timezone.now)
    role = models.CharField(max_length=100,null=False,default='user')
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stripe_id = models.CharField(max_length=300, null=True,editable=True)

    def __str__(self):
        return f"User (`{self.first_name}`, `{self.middle_name}`. `{self.last_name}`, `{self.email}`, `{self.username}`, `{self.role}` , `{self.user_id}` `{self.timestamp}` )"
