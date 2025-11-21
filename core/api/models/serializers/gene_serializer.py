# core/api/serializers/gene_serializer.py

from rest_framework import serializers
from ..entities.gene import Gene  # Import relativo correcto dentro de la app 'api'

class GeneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gene
        fields = ['id', 'symbol', 'fullName', 'functionSummary']
