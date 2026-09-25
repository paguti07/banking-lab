class InsufficientFundsError(Exception):
    def __init__(self, message: str, amount: float = None):
        self.amount = amount
        super().__init__(message)
