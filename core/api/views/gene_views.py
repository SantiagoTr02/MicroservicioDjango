# python
from rest_framework import viewsets
from ..models.entities.gene import Gene
from ..models.serializers.gene_serializer import GeneSerializer

class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
