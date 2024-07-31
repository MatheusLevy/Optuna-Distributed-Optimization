class KernelExceptions(Exception):
    def __init__(self, message="", details=None, error=None):
        super().__init__(message)  # Passa a messagem base para a classe Exception
        self.message = message
        self.details = details
        self.error = error
    
    def __str__(self):
        return f'{self.message} Details: {self.details} on Error: {self.error}'