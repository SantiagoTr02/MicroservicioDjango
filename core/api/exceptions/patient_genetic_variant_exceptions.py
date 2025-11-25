class PatientGeneticVariantAlreadyExistsException(Exception):
    #Excepcion para cuando la variante genética ya ha sido asignada al paciente
    def __init__(self, message="This genetic variant has already been assigned to the patient"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PatientGeneticVariantFieldNotFilledException(Exception):
    #Excepcion para cuando hay un campo obligatorio no rellenado
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class PatientGeneticVariantInvalidDataFormatException(Exception):
    #Excepcion para cuando se ingresa un dato invalido
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
