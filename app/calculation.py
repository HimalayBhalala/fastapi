def sum(a: int,b: int):
    return a+b

def sub(a: int,b: int):
    return a-b

def mul(a: int,b: int):
    return a*b

def div(a: int,b: int):
    return a/b


class BankAccount:
    def __init__(self,balance=0):
        self.balance = balance
        
    def money_deposit(self,money):
        self.balance += money
        
    def money_withdraw(self,money):
        if self.balance < money:
            raise Exception("Insufficient balance in your account")
        self.balance -= money
        
    def money_interest(self):
        self.balance *= (1.1)