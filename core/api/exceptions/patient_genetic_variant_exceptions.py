# core/api/exceptions/patient_genetic_variant_exceptions.py

class PatientGeneticVariantAlreadyExistsException(Exception):
    """Se lanza cuando la variante genética ya ha sido asignada al paciente."""
    def __init__(self, message="This genetic variant has already been assigned to the patient"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PatientGeneticVariantFieldNotFilledException(Exception):
    """Campo obligatorio no rellenado en PatientGeneticVariant."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PatientGeneticVariantInvalidDataFormatException(Exception):
    """Formato de dato inválido en PatientGeneticVariant."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
