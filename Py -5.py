class Atm:
    def __init__(self, balance):
        self.__balance = balance
        self.balance = balance

    def show_balance(self):
        print(f"Current balance: ${self.balance}")

    def deposit_amount(self, deposit_amount):
        self.balance += deposit_amount
        print(f"Deposited: ${deposit_amount}. New balance: ${self.balance}")

    def withdraw_amount(self, withdraw_amount):
        self.balance -= withdraw_amount
        print(f"Withdrew: ${withdraw_amount}. New balance: ${self.balance}")


obj1 = Atm(1000)
obj1.show_balance()
obj1.deposit_amount(500)
obj1.withdraw_amount(2000)

print(obj1._Atm__balance) 
