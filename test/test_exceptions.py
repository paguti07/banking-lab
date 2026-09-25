import pytest

from exceptions import InsufficientFundsError


def test_stores_amount():
    err = InsufficientFundsError("not enough funds", 42.5)
    assert err.amount == 42.5


def test_amount_defaults_to_none():
    # several call sites in bank_account.py raise with only a message
    err = InsufficientFundsError("not enough funds")
    assert err.amount is None


def test_message_is_preserved():
    err = InsufficientFundsError("not enough funds", 10)
    assert str(err) == "not enough funds"


def test_is_a_real_exception():
    with pytest.raises(InsufficientFundsError):
        raise InsufficientFundsError("boom")