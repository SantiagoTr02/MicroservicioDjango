# core/api/models/gene.py

from django.db import models

class Gene(models.Model):
    symbol = models.CharField(max_length=50, unique=True)
    fullName = models.CharField(max_length=150, blank=True, null=True)
    functionSummary = models.TextField(blank=True, null=True)

    class Meta:
        managed = False  # No se migran las tablas, se usan las existentes
        db_table = 'gene'  # El nombre de la tabla tal cual como está en la base de datos
