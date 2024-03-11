from app.calculation import div,mul,sub,sum,BankAccount
import pytest


# @pytest.mark.parametrize("num1,num2,result",[(1,10,11),(100,1,101),(190,10,200)])
# def test_sum(num1,num2,result):
#     print("tests is sum success")
#     assert sum(num1,num2) == result


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(1000)

def test_zero_bank_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_balance(bank_account):
    assert bank_account.balance == 1000
    
def test_bank_deposit(bank_account):
    bank_account.money_deposit(10000)
    print(bank_account.balance)
    assert bank_account.balance == 11000
    
def test_bank_withdraw():
    bank = BankAccount(1000)
    bank.money_withdraw(500)
    assert bank.balance == 500
    
def test_bank_interest():
    bank = BankAccount(1000)
    bank.money_interest()
    assert bank.balance == 1100
    
    
@pytest.mark.parametrize("deposit,withdraw,expected",[
    (100,10,90),
    (1000,100,900)
])
def test_bank_transaction(zero_bank_account,deposit,withdraw,expected):
    zero_bank_account.money_deposit(deposit)
    zero_bank_account.money_withdraw(withdraw)
    print(zero_bank_account.balance)
    assert zero_bank_account.balance == expected