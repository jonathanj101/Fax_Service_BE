from rest_framework import serializers
from api.models.temporary_file_model import TemporaryFilesModel


class TempoaryFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryFilesModel
        field = ["__all__"]
