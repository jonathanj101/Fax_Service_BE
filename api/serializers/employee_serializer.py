from rest_framework import serializers
from api.models.employee_model import EmployeeModel


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = ["user_id", "company_id", "timestamp"]
