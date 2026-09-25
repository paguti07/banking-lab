import datetime
from datetime import date, timedelta

import pytest

from bank_account import BankAccount
from customer import Customer
from exceptions import InsufficientFundsError


class TestConstruction:
    def test_adult_customer_is_created(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        assert customer.user_id == 1
        assert customer.accounts == []

    def test_minor_raises_value_error(self, minor_birth_date):
        with pytest.raises(ValueError):
            Customer("Kid", minor_birth_date)

    def test_user_ids_increment_sequentially(self, adult_birth_date):
        c1 = Customer("Alice", adult_birth_date)
        c2 = Customer("Bob", adult_birth_date)
        assert c2.user_id == c1.user_id + 1

    def test_exactly_18_today_is_allowed(self):
        today = datetime.datetime.now(tz=None).date()
        birth_date = today.replace(year=today.year - 18)
        customer = Customer("Just Eighteen", birth_date)
        assert customer.user_id == 1

    def test_turning_18_tomorrow_is_still_a_minor(self):
        today = datetime.datetime.now(tz=None).date()
        birth_date = today.replace(year=today.year - 18) + timedelta(days=1)
        with pytest.raises(ValueError):
            Customer("Almost 18", birth_date)

    def test_repr_is_a_string(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        assert isinstance(repr(customer), str)


class TestCalculateAge:
    def test_birthday_already_passed_this_year(self):
        on_date = date(2026, 6, 15)
        birth_date = date(1990, 6, 14)
        assert Customer.calculate_age(birth_date, on_date=on_date) == 36

    def test_birthday_not_yet_reached_this_year(self):
        on_date = date(2026, 6, 15)
        birth_date = date(1990, 6, 16)
        assert Customer.calculate_age(birth_date, on_date=on_date) == 35

    def test_birthday_is_today(self):
        on_date = date(2026, 6, 15)
        birth_date = date(1990, 6, 15)
        assert Customer.calculate_age(birth_date, on_date=on_date) == 36


class TestAddAccount:
    def test_valid_account_is_added(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        account = BankAccount("1234567890")
        customer.add_account(account)
        assert account in customer.accounts

    def test_invalid_account_number_is_rejected(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        account = BankAccount("123")  # not 10 digits
        customer.add_account(account)
        assert account not in customer.accounts


class TestGetTotalBalance:
    def test_sums_all_accounts(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        customer.add_account(BankAccount("1111111111", balance=100.0))
        customer.add_account(BankAccount("2222222222", balance=250.0))
        assert customer.get_total_balance() == 350.0

    def test_zero_with_no_accounts(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        assert customer.get_total_balance() == 0.0


class TestTransfer:
    def test_moves_money_between_owned_accounts(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        source = BankAccount("1111111111", balance=200.0)
        target = BankAccount("2222222222", balance=0.0)
        customer.add_account(source)
        customer.add_account(target)

        customer.transfer(source, target, 50.0)

        assert source.balance == 150.0
        assert target.balance == 50.0

    def test_rejects_source_account_not_owned_by_customer(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        owned = BankAccount("1111111111", balance=200.0)
        customer.add_account(owned)
        someone_elses = BankAccount("3333333333", balance=0.0)

        customer.transfer(someone_elses, owned, 50.0)

        assert owned.balance == 200.0  # unchanged, transfer was rejected

    def test_insufficient_funds_propagates(self, adult_birth_date):
        customer = Customer("Alice", adult_birth_date)
        source = BankAccount("1111111111", balance=10.0)
        target = BankAccount("2222222222", balance=0.0)
        customer.add_account(source)
        customer.add_account(target)

        with pytest.raises(InsufficientFundsError):
            customer.transfer(source, target, 1000.0)
