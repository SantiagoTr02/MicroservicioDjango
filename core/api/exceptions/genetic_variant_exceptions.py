# core/api/exceptions/genetic_variant_exceptions.py

class GeneticVariantFieldNotFilledException(Exception):
    """Campo obligatorio no rellenado en GeneticVariant."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneticVariantInvalidDataFormatException(Exception):
    """Formato de dato inválido en GeneticVariant."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneNotFoundException(Exception):
    """El Gene asociado a la variante no existe."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneticVariantNotFoundException(Exception):
    """La variante genética no existe."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class GeneticVariantDeletionNotAllowedException(Exception):
    """No se puede eliminar la variante (por ejemplo, tiene asociaciones)."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


# core/api/exceptions/genetic_variant_exceptions.py

class GeneticVariantAlreadyExistsException(Exception):
    """Se lanza cuando se intenta crear una variante genética duplicada."""
    def __init__(self, message="Genetic variant already exists with the same data"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneForVariantNotFoundException(Exception):
    """Se lanza cuando el geneId asociado a la variante no existe."""
    def __init__(self, message="Gene for this variant was not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
