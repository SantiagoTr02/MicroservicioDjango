import uuid

from django.db import models

class GeneticVariant(models.Model):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)  # UUID para el id
    geneId = models.ForeignKey('Gene', on_delete=models.CASCADE)  # Relación con Gene
    chromosome = models.CharField(max_length=50)
    position = models.IntegerField()
    referenceBase = models.CharField(max_length=1)
    alternateBase = models.CharField(max_length=1)
    impact = models.CharField(max_length=50)

    class Meta:
        managed = False  # No gestionamos las migraciones, se usa la base existente
        db_table = 'geneticvariant'  # Nombre de la tabla tal como está en la base de datos
