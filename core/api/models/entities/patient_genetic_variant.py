
from django.db import models
from uuid import uuid4
from .patient import Patient
from .genetic_variant import GeneticVariant

class PatientGeneticVariant(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        db_column='id',
        default=uuid4
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        db_column='patientId'
    )


    variant = models.ForeignKey(
        GeneticVariant,
        on_delete=models.CASCADE,
        db_column='variantId'
    )

    detectionDate = models.DateField(db_column='detectionDate')
    alleleFrequency = models.DecimalField(
        max_digits=5,
        decimal_places=4,
        null=True,
        blank=True,
        db_column='alleleFrequency'
    )

    class Meta:
        managed = False
        db_table = 'patientvariantreport'

    def __str__(self):
        return f"Variant {self.variant.id} assigned to Patient {self.patient.firstName} {self.patient.lastName}"
