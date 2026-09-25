import pytest

from bank_account import BankAccount
from exceptions import InsufficientFundsError


class TestConstruction:
    def test_defaults(self):
        acct = BankAccount("1234567890")
        assert acct.account_number == "1234567890"
        assert acct.currency == "USD"
        assert acct.account_type == "checking"
        assert acct.balance == 0.0

    def test_custom_values(self):
        acct = BankAccount(
            "1234567890", currency="EUR", account_type="checking", balance=250.0
        )
        assert acct.currency == "EUR"
        assert acct.balance == 250.0

    def test_savings_below_100_raises_insufficient_funds(self):
        with pytest.raises(InsufficientFundsError):
            BankAccount("1234567890", account_type="savings", balance=50.0)

    def test_savings_at_100_is_allowed(self):
        acct = BankAccount("1234567890", account_type="savings", balance=100.0)
        assert acct.balance == 100.0


class TestBalanceSetter:
    def test_negative_balance_raises_value_error(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(ValueError):
            acct.balance = -1.0

    def test_zero_is_allowed(self):
        acct = BankAccount("1234567890", balance=100.0)
        acct.balance = 0.0
        assert acct.balance == 0.0


class TestDeposit:
    def test_deposit_increases_balance(self):
        acct = BankAccount("1234567890", balance=100.0)
        acct.deposit(50.0)
        assert acct.balance == 150.0

    def test_negative_deposit_raises_value_error(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(ValueError):
            acct.deposit(-10.0)

    def test_zero_deposit_raises_value_error(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(ValueError):
            acct.deposit(0.0)


class TestWithdraw:
    def test_withdraw_decreases_balance(self):
        acct = BankAccount("1234567890", balance=100.0)
        acct.withdraw(40.0)
        assert acct.balance == 60.0

    def test_withdraw_more_than_balance_raises_insufficient_funds(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(InsufficientFundsError):
            acct.withdraw(200.0)

    def test_negative_withdraw_raises_value_error(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(ValueError):
            acct.withdraw(-5.0)

    def test_savings_cannot_drop_below_100(self):
        acct = BankAccount("1234567890", account_type="savings", balance=150.0)
        with pytest.raises(InsufficientFundsError):
            acct.withdraw(60.0)  # would leave 90

    def test_savings_can_withdraw_down_to_exactly_100(self):
        acct = BankAccount("1234567890", account_type="savings", balance=150.0)
        acct.withdraw(50.0)
        assert acct.balance == 100.0


class TestConvertCurrency:
    def test_zero_exchange_rate_raises_value_error(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(ValueError):
            acct.convert_currency("EUR", 0.0)

    def test_negative_exchange_rate_raises_value_error(self):
        acct = BankAccount("1234567890", balance=100.0)
        with pytest.raises(ValueError):
            acct.convert_currency("EUR", -0.9)

    def test_valid_conversion_prints_result(self, capsys):
        acct = BankAccount("1234567890", balance=100.0)
        acct.convert_currency("EUR", 0.9)
        captured = capsys.readouterr()
        assert "90" in captured.out


class TestCreateSavings:
    def test_returns_a_bank_account(self):
        acct = BankAccount.create_savings("1234567890")
        assert isinstance(acct, BankAccount)
        assert acct.account_type == "savings"
        assert acct.balance == 100.0

    def test_below_minimum_raises_insufficient_funds(self):
        with pytest.raises(InsufficientFundsError):
            BankAccount.create_savings("1234567890", balance=50.0)


class TestIsValidAccountNumber:
    @pytest.mark.parametrize(
        "number,expected",
        [
            ("1234567890", True),
            ("12345", False),  # too short
            ("12345678901", False),  # too long
            ("12345abcde", False),  # not all digits
            ("", False),
        ],
    )
    def test_validation(self, number, expected):
        assert BankAccount.is_valid_account_number(number) is expected
