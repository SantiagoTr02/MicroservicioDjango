# core/api/exceptions/gene_exceptions.py

class FieldNotFilledException(Exception):
    #Excepción  para campos obligatorios que no se han ingresado
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidDataFormatException(Exception):
    #Excepción para campos inválidos
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneNotFoundException(Exception):
    #Excepción para cuando no se encuentra un gene
    def __init__(self, message="Gene not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NoFieldsToUpdateException(Exception):
    #Excepción cuando no se envía ningun campo para actualizar
    def __init__(self, message="No fields provided to update"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneSymbolAlreadyExistsException(Exception):
    #Excepcion cuando el simbolo de un Gene ya existe
    def __init__(self, message="Gene symbol already exists"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
