# core/api/serializers/genetic_variant_serializer.py

from rest_framework import serializers
from ..entities.genetic_variant import GeneticVariant  # Import relativo correcto dentro de la app 'api'

class GeneticVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneticVariant
        fields = [
            'id',
            'geneId',
            'chromosome',
            'position',
            'referenceBase',
            'alternateBase',
            'impact'
        ]
