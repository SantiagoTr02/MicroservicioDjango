# core/api/exceptions/gene_exceptions.py

class FieldNotFilledException(Exception):
    """Excepción personalizada para campos no rellenados en Gene"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class InvalidDataFormatException(Exception):
    """Excepción personalizada para formato de datos inválidos en Gene"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class GeneNotFoundException(Exception):
    """Excepción personalizada para cuando no se encuentra un Gene"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
