# this file is only for demonstrating the usage of pytest library
# in tests/test_calculations.py


def add(num1: int, num2: int):
    return num1 + num2


def subtract(num1: int, num2: int):
    return num1 - num2


def multiply(num1: int, num2: int):
    return num1 * num2


def divide(num1: int, num2: int):
    return num1 / num2


class InsufficientFunds(Exception):
    pass


class BankAccount:
    def __init__(self, starting_balance=0) -> None:
        self.balance = starting_balance
        self.interest_rate = 1.1

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds in account")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= self.interest_rate
