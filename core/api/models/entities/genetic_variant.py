# core/api/models/genetic_variant.py

from django.db import models

class GeneticVariant(models.Model):
    id = models.AutoField(primary_key=True)  # AUTO_INCREMENT
    geneId = models.ForeignKey('Gene', on_delete=models.CASCADE)  # Relación con la tabla Gene
    chromosome = models.CharField(max_length=50)
    position = models.IntegerField()
    referenceBase = models.CharField(max_length=1)
    alternateBase = models.CharField(max_length=1)
    impact = models.CharField(max_length=50)

    class Meta:
        managed = False  # No se migran las tablas, se usan las existentes
        db_table = 'geneticvariant'  # Nombre de la tabla tal cual como está en la base de datos
