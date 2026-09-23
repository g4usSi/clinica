from rest_framework import serializers

from .models import Medicamento


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ["id", "name", "description", "stock", "price", "created_at"]
        read_only_fields = ["id", "created_at"]
