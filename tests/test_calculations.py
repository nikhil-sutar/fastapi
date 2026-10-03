import pytest
from app.calculations import add, BankAccount

@pytest.fixture
def zero_bank_account():
    print("creating bank account with zero balance.")
    return BankAccount()

@pytest.fixture
def bank_account():
    print("creating bank account with balance 50")
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
    (5,6,11),
    (1,4,5),
    (45,6,51),
])
def test_add(num1, num2, expected):
    assert add(num1,num2) == expected

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_insufficient_balance(bank_account):
    with pytest.raises(Exception):
        bank_account.withdraw(200)

