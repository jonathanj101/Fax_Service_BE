from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import DO_NOTHING
from django.utils import timezone
import uuid

class CompanyModel(models.Model):
    business_name = models.CharField(max_length=100,null=False)
    business_street_address = models.CharField(max_length=200,null=False)
    business_registered_country = models.CharField(max_length=100,null=False)
    business_registered_city = models.CharField(max_length=100,null=False)
    business_registered_zipcode = models.CharField(max_length=100,null=False)
    business_contact_number = models.CharField(max_length=100,null=False)
    business_email = models.CharField(max_length=100,null=True)
    business_fax_number = models.CharField(max_length=100,null=False)
    business_owner = models.ForeignKey("UserModel", on_delete=DO_NOTHING, null=False)
    business_type = models.CharField(max_length=100,null=False, default="retail")
    business_size = models.FloatField()
    timestamp = models.DateField(blank=True,default=timezone.now)
    business_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"('{self.pk}', '{self.business_name}', '{self.business_street_address}','{self.business_registered_country}','{self.business_registered_city}', '{self.business_registered_zipcode}', '{self.business_contact_number}', '{self.business_email}', '{self.business_fax_number}', {self.business_type}', {self.business_size}', {self.business_id}', {self.business_owner}', {self.timestamp}', )"
