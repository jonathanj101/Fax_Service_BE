from rest_framework import serializers
from api.models.company_model import CompanyModel

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = ["__all__"]