from rest_framework import serializers
from ..entities.genetic_variant import GeneticVariant

class GeneticVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneticVariant
        fields = ['id', 'geneId', 'chromosome', 'position', 'referenceBase', 'alternateBase', 'impact']
