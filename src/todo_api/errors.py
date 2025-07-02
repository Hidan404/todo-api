# src/errors.py
class APIError(Exception):
    def __init__(self, message: str, status_code: int = 500, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload  # Para detalhes adicionais

    def to_dict(self):
        rv = {
            "success": False,
            "error": self.message,
            "status_code": self.status_code
        }
        if self.payload:
            rv["details"] = self.payload
        return rv
    
    def __str__(self):
        return f"{self.status_code} - {self.message}"