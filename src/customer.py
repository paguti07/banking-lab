from datetime import date
from itertools import count

from bank_account import BankAccount
from logger import Logger


class Customer:
    user_count = count(1)

    def __init__(self, name: str, birth_date: date):
        if Customer.calculate_age(birth_date) < 18:
            raise ValueError("Customer must be at least 18 years old")
        self._user_id = next(Customer.user_count)
        self.__accounts = []
        self.name = name
        self.logger = Logger().get_logger

    @staticmethod
    def calculate_age(birth_date: date, on_date: date | None = None) -> int:
        on_date = on_date or date.today() # noqa: DTZ011 — birth dates don't need a timezone
        age = on_date.year - birth_date.year
        # subtract 1 if birthday hasn't happened yet this year
        if (on_date.month, on_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age

    @property
    def user_id(self):
        return self._user_id

    @property
    def accounts(self):
        return self.__accounts

    def add_account(self, account: BankAccount):
        if BankAccount.is_valid_account_number(account.account_number):
            self.__accounts.append(account)
        else:
            self.logger.error(f"Invalid account number {account.account_number}")

    def get_total_balance(self) -> float:
        return sum(acc.balance for acc in self.__accounts)

    def transfer(self, source_account, target_account, amount: float):
        if source_account not in self.__accounts:
            self.logger.error(
                f"Transfer failed: source account {source_account.account_number} not owned by this customer"
            )
            return
        source_account.withdraw(amount)
        target_account.deposit(amount)

    def __repr__(self):
        return str(self.user_id)
