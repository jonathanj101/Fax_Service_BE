from rest_framework import serializers
from api.models.company_model import CompanyModel


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = [
            "business_name",
            "business_street_address",
            "business_registered_country",
            "business_registered_city",
            "business_registered_zipcode",
            "business_contact_number",
            "business_email",
            "business_fax_number",
            "business_owner",
            "business_type",
            "business_size",
            "business_id",
        ]
