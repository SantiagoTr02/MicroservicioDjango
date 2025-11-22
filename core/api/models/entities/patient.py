from django.db import models
import uuid

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Asegúrate de que este es un UUID
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    birthDate = models.DateField()
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    status = models.CharField(max_length=11, choices=[('Activo', 'Activo'), ('Seguimiento', 'Seguimiento')])


    class Meta:
        db_table = 'patient'  # Nombre de la tabla tal como está en la base de datos
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
