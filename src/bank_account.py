from exceptions import InsufficientFundsError
from logger import Logger


class BankAccount:
    def __init__(
        self,
        account_number: str,
        currency: str = "USD",
        account_type: str = "checking",
        balance: float = 0.0,
    ):
        if account_type == "savings" and balance < 100:
            raise InsufficientFundsError(
                "Savings account balance can never fall below $100", balance
            )

        self.logger = Logger().get_logger
        self._account_number = account_number
        self._account_type = account_type
        self._currency = currency
        self.__balance = balance

    @property
    def account_number(self):
        return self._account_number

    @property
    def currency(self):
        return self._currency

    @property
    def account_type(self):
        return self._account_type

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, value: float):
        if value >= 0.0:
            self.__balance = value
        else:
            self.logger.error(
                f"Negative balance not allowed. Amount={self.currency}: {value}"
            )
            raise ValueError("Negative balance not allowed", value)

    def deposit(self, value: float):
        if value > 0.0:
            self.balance = value + self.balance
            self.logger.info(
                f"New balance after deposit = {self.currency}: {self.balance}"
            )
        else:
            self.logger.error("Negative deposit not allowed")
            raise ValueError("Negative deposit not allowed")

    def withdraw(self, value: float):
        if value > 0.0:
            if value <= self.balance:
                if self.account_type == "savings" and (self.balance - value) < 100:
                    self.logger.error(
                        "Savings account balance can never fall below $100"
                    )
                    raise InsufficientFundsError(
                        "Savings account balance can never fall below $100"
                    )
                self.balance = self.balance - value
                self.logger.info(
                    f"New balance after withdraw = {self.currency}: {self.balance}"
                )
            else:
                self.logger.error(
                    f"Insufficient funds for withdrawal. Amount={self.currency}: {value}"
                )
                raise InsufficientFundsError("Insufficient funds for withdrawal", value)
        else:
            self.logger.error("Negative withdraw not allowed")
            raise ValueError("Negative withdraw not allowed")

    def convert_currency(self, target_currency: str, exchange_rate: float):
        if exchange_rate <= 0.0:
            self.logger.error("Exchange rate must be greater than zero")
            raise ValueError("Exchange rate must be greater than zero")
        print(f"Balance in {target_currency} is {exchange_rate * self.balance}")

    @classmethod
    def create_savings(
        cls,
        account_number: str,
        currency: str = "USD",
        account_type: str = "savings",
        balance: float = 100.0,
    ):
        if account_type == "savings" and balance < 100:
            raise InsufficientFundsError(
                "Savings account balance can never fall below $100", balance
            )

        return cls(
            account_number=account_number,
            currency=currency,
            account_type=account_type,
            balance=balance,
        )

    @staticmethod
    def is_valid_account_number(account_number: str):
        return bool(account_number.isdigit() and len(account_number) == 10)
