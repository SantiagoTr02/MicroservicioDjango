# core/api/exceptions/gene_exceptions.py

class FieldNotFilledException(Exception):
    """Excepción personalizada para campos no rellenados en Gene"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidDataFormatException(Exception):
    """Excepción personalizada para formato de datos inválidos en Gene"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneNotFoundException(Exception):
    """Excepción personalizada para cuando no se encuentra un Gene"""
    def __init__(self, message="Gene not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NoFieldsToUpdateException(Exception):
    """Excepción cuando no se envía ningún campo para actualizar un Gene"""
    def __init__(self, message="No fields provided to update"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneSymbolAlreadyExistsException(Exception):
    """Excepción cuando el símbolo de un Gene ya existe"""
    def __init__(self, message="Gene symbol already exists"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
