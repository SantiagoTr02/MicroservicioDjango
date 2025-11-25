class GeneticVariantFieldNotFilledException(Exception):
    #Excepción  para campos obligatorios que no se han ingresado
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneticVariantInvalidDataFormatException(Exception):
    #Excepción para campos con formato invalido
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneNotFoundException(Exception):
    #Excepcion para cuando el gene asociado a la variante no existe
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneticVariantNotFoundException(Exception):
    #Excepcion para cuando la variante genetica no existe
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class GeneticVariantDeletionNotAllowedException(Exception):
    #Excepcion para cuando no se puede eliminar la variante
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class GeneticVariantAlreadyExistsException(Exception):
    #Excepcion para cuando se intenta crear una variante genetica duplicada
    def __init__(self, message="Genetic variant already exists with the same data"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class GeneForVariantNotFoundException(Exception):
    #Excepcion para cuando el geneId asociado a la variante no existe
    def __init__(self, message="Gene for this variant was not found"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
