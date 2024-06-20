class KernelExceptions(Exception):
    def __init__(self, mensage, details=None, error=None):
        self.mensage = mensage
        self.details = details
        self.error = error
    
    def __str__(self):
        return f'{self.mensage}. Details: {self.details} on Error: {self.error}'