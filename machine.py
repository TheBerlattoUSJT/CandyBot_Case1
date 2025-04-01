import pygame

class CandyMachine:
    def __init__(self):
        self.states = ["Waiting", "Selecting", "Dispensing", "Returning Change"]
        self.current_state = "Waiting"
        self.balance = 0
        self.returnChangeBalance = 0
        self.candies = {
            "A": {"price": 6, "stock": 5},
            "B": {"price": 7, "stock": 5},
            "C": {"price": 8, "stock": 5}
        }
        self.valid_coins = [1, 2, 5]

    def insert_money(self, amount):
        if amount in self.valid_coins:
            self.balance += amount
            print(f"Inserted R$ {amount}. Current balance: R$ {self.balance}")
            self.current_state = "Selecting"
        else:
            print("Invalid money!")

    def select_candy(self, candy):
        if self.current_state != "Selecting":
            print("Insuficient Money!")
            return

        if candy not in self.candies:
            print("Candy not found!")
            return

        price = self.candies[candy]["price"]

        if self.balance >= price and self.candies[candy]["stock"] > 0:
            self.balance -= price
            self.candies[candy]["stock"] -= 1
            print(f"Dropando Candy {candy}. Current Money: R$ {self.balance}")
            self.current_state = "Dispensing"

            if self.balance > 0:
                self.current_state = "Returning Change"
                self.return_change()
            else:
                self.current_state = "Waiting"
        else:
            print(f"Insuficient money for Candy {candy} (R$ {price}).")

    def return_change(self):
        # saldo zerar pos compra ou deixar o usuario comprar mais?
        # por enquanto apenas zerar ao comprar
        if self.balance > 0:
            print(f"Returning change: R$ {self.balance}")
            self.returnChangeBalance = self.balance
            self.balance = 0
        self.current_state = "Waiting"

    def reset_machine(self):
        self.current_state = "Waiting"
        self.balance = 0
        print("Machine reset.")